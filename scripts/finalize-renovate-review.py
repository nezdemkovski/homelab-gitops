#!/usr/bin/env python3
"""Apply a Claude verdict to one Renovate PR and merge only a safe current head."""

import json
import os
import subprocess
import sys
from urllib.parse import quote, urlparse

MARKER = "<!-- automated-renovate-review -->"
BOT = "nezdemkovski-renovate[bot]"
LABELS = {
    "review/approved": "2da44e",
    "review/needs-human": "d73a4a",
    "risk/breaking-change": "f6412d",
    "risk/migration": "ff9800",
}


def gh(*args: str, data: object | None = None) -> object:
    command = ["gh", "api", *args]
    result = subprocess.run(
        command,
        input=json.dumps(data) if data is not None else None,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(f"gh {' '.join(args)}: {result.stderr.strip()}")
    return json.loads(result.stdout) if result.stdout.strip() else None


def usable_source(source: str) -> bool:
    try:
        url = urlparse(source)
        hostname = url.hostname
    except ValueError:
        return False
    return (
        url.scheme == "https"
        and bool(hostname)
        and hostname not in {"example.com", "example.org", "example.net"}
        and not hostname.endswith((".example.com", ".example.org", ".example.net"))
    )


def review() -> tuple[dict, str | None]:
    if os.environ.get("CLAUDE_OUTCOME") != "success":
        return {}, "Claude review did not complete"
    try:
        data = json.loads(os.environ.get("REVIEW_JSON", ""))
    except json.JSONDecodeError:
        return {}, "Claude did not return valid JSON"
    required = {
        "verdict": str,
        "breaking_change": bool,
        "migration_required": bool,
        "summary": str,
        "findings": list,
        "sources": list,
    }
    if not isinstance(data, dict) or any(
        key not in data or type(data[key]) is not kind
        for key, kind in required.items()
    ):
        return {}, "Claude returned an incomplete review"
    if data["verdict"] not in ("approve", "needs-human"):
        return {}, "Claude returned an unknown verdict"
    if not data["summary"].strip():
        return {}, "Claude returned no explanation"
    if any(not isinstance(item, str) for item in data["findings"] + data["sources"]):
        return {}, "Claude returned malformed findings or sources"
    summary = data["summary"].strip().lower()
    placeholder_summary = summary in {"test", "test summary", "placeholder", "todo", "n/a"}
    invalid_sources = any(not usable_source(source) for source in data["sources"])
    if placeholder_summary or invalid_sources or (
        data["verdict"] == "approve" and not data["sources"]
    ):
        # Do not publish an invalid model response as review evidence.
        return {}, "Claude returned no usable review evidence"
    if data["verdict"] == "approve" and (
        data["breaking_change"] or data["migration_required"]
    ):
        return data, "Breaking change or migration requires human review"
    return data, None


def ensure_labels(repo: str) -> None:
    for name, color in LABELS.items():
        result = subprocess.run(
            ["gh", "api", "-X", "POST", f"repos/{repo}/labels",
             "--input", "-"],
            input=json.dumps({"name": name, "color": color}),
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode and "already_exists" not in result.stderr:
            # GitHub returns 422 when the label already exists.
            existing = gh(f"repos/{repo}/labels/{quote(name, safe='')}")
            if not isinstance(existing, dict) or existing.get("name") != name:
                raise RuntimeError(f"Could not create label {name}: {result.stderr}")


def set_labels(repo: str, number: int, desired: list[str]) -> None:
    current = gh(f"repos/{repo}/issues/{number}/labels?per_page=100")
    for label in current:
        name = label["name"]
        if name in LABELS and name not in desired:
            gh("-X", "DELETE", f"repos/{repo}/issues/{number}/labels/"
               f"{quote(name, safe='')}")
    if desired:
        gh("-X", "POST", f"repos/{repo}/issues/{number}/labels",
           "--input", "-", data={"labels": desired})


def comment_body(data: dict, verdict: str, reason: str | None) -> str:
    if data:
        details = data["summary"].strip()[:4000]
        findings = data["findings"]
        sources = data["sources"]
    else:
        details, findings, sources = reason or "Review unavailable", [], []
    lines = [MARKER, f"**Claude verdict:** {verdict}", "", details]
    if reason and data:
        lines += ["", f"**Automatic merge stopped:** {reason}"]
    if findings:
        lines += ["", "**Findings**"]
        lines += [f"- {item[:1000]}" for item in findings[:20]]
    if sources:
        lines += ["", "**Sources**"]
        lines += [f"- {item[:500]}" for item in sources[:20]]
    return "\n".join(lines)


def upsert_comment(repo: str, number: int, body: str) -> None:
    comments = gh(f"repos/{repo}/issues/{number}/comments?per_page=100")
    previous = next(
        (item for item in comments
         if item.get("user", {}).get("login") == BOT
         and item.get("body", "").startswith(MARKER)),
        None,
    )
    if previous:
        gh("-X", "PATCH", f"repos/{repo}/issues/comments/{previous['id']}",
           "--input", "-", data={"body": body})
    else:
        gh("-X", "POST", f"repos/{repo}/issues/{number}/comments",
           "--input", "-", data={"body": body})


def main() -> int:
    repo = os.environ["GITHUB_REPOSITORY"]
    number = int(os.environ["PR_NUMBER"])
    expected_sha = os.environ["EXPECTED_SHA"]
    expected_base_sha = os.environ["EXPECTED_BASE_SHA"]
    pr = gh(f"repos/{repo}/pulls/{number}")
    if (
        pr["state"] != "open"
        or pr["draft"]
        or pr["base"]["ref"] != "master"
        or pr["base"]["sha"] != expected_base_sha
        or pr["head"]["sha"] != expected_sha
        or pr["head"]["repo"]["full_name"] != repo
        or pr["head"]["ref"].startswith("renovate/") is False
        or pr["user"]["login"] != BOT
    ):
        print("PR changed or is not a current Renovate PR; no action taken")
        return 0

    data, reason = review()
    stale_base = False
    if data.get("verdict") == "approve" and reason is None:
        if any(label["name"] == "type/major" for label in pr.get("labels", [])):
            reason = "Major update requires verified backup and human merge"
        else:
            current_base = gh(f"repos/{repo}/git/ref/heads/master")["object"]["sha"]
            stale_base = current_base != expected_base_sha
            if stale_base:
                reason = "Base branch advanced; Renovate will rebase and review again"
            else:
                files = gh(f"repos/{repo}/pulls/{number}/files?per_page=100")
                if len(files) == 100:
                    reason = "PR has 100 or more files; merge eligibility needs human review"
                elif any(item["filename"].startswith(".github/workflows/") for item in files):
                    reason = "GitHub App cannot merge workflow changes without workflows permission"
    claude_verdict = {
        "approve": "approved",
        "needs-human": "needs human review",
    }.get(data.get("verdict"), "unavailable")
    verdict = (
        "approved"
        if data.get("verdict") == "approve" and reason is None
        else "needs human review"
    )
    desired = [] if stale_base else [
        "review/approved" if verdict == "approved" else "review/needs-human"
    ]
    if data.get("breaking_change"):
        desired.append("risk/breaking-change")
    if data.get("migration_required"):
        desired.append("risk/migration")

    ensure_labels(repo)
    set_labels(repo, number, desired)
    upsert_comment(repo, number, comment_body(data, claude_verdict, reason))
    if verdict != "approved":
        print("Review did not approve; PR remains open")
        return 0

    result = subprocess.run(
        ["gh", "pr", "merge", str(number), "--repo", repo,
         "--squash", "--match-head-commit", expected_sha],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        base_changed = "Base branch was modified" in result.stderr
        set_labels(repo, number, [] if base_changed else ["review/needs-human"])
        upsert_comment(
            repo, number,
            comment_body(data, claude_verdict,
                         "Base branch advanced; Renovate will rebase and review again"
                         if base_changed else
                         f"GitHub could not merge the approved PR: "
                         f"{result.stderr.strip()[:1000]}"),
        )
        print(result.stderr, file=sys.stderr)
        return 0 if base_changed else 1
    print(f"Merged approved Renovate PR #{number} at {expected_sha}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
