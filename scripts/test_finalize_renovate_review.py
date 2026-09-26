"""Offline checks for the trusted Renovate review gate."""

import importlib.util
import json
import unittest
from pathlib import Path
from unittest.mock import patch


SPEC = importlib.util.spec_from_file_location(
    "review_gate", Path(__file__).with_name("finalize-renovate-review.py")
)
gate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gate)


class ReviewTests(unittest.TestCase):
    def review(self, **changes):
        response = {
            "verdict": "approve",
            "breaking_change": False,
            "migration_required": False,
            "summary": "The release only updates the action runtime dependency.",
            "findings": ["No workflow inputs or permissions changed."],
            "sources": ["https://github.com/anthropics/claude-code-action/releases"],
        }
        response.update(changes)
        with patch.dict(
            "os.environ",
            {"CLAUDE_OUTCOME": "success", "REVIEW_JSON": json.dumps(response)},
        ):
            return gate.review()

    def test_real_approval_keeps_evidence(self):
        data, reason = self.review()
        self.assertEqual(data["verdict"], "approve")
        self.assertIsNone(reason)

    def test_placeholder_approval_is_not_published_as_evidence(self):
        data, reason = self.review(
            summary="Test", findings=["a", "b"], sources=["https://example.com"]
        )
        self.assertEqual(data, {})
        self.assertEqual(reason, "Claude returned no usable review evidence")
        body = gate.comment_body(data, "needs human review", reason)
        self.assertNotIn("**Findings**", body)
        self.assertNotIn("example.com", body)

    def test_placeholder_human_review_is_not_published(self):
        data, reason = self.review(verdict="needs-human", sources=["https://example.com"])
        self.assertEqual(data, {})
        self.assertEqual(reason, "Claude returned no usable review evidence")

    def test_real_human_review_can_lack_sources(self):
        data, reason = self.review(
            verdict="needs-human",
            summary="Release notes were unavailable, so compatibility is uncertain.",
            findings=["The release range could not be verified."],
            sources=[],
        )
        self.assertEqual(data["verdict"], "needs-human")
        self.assertIsNone(reason)


if __name__ == "__main__":
    unittest.main()
