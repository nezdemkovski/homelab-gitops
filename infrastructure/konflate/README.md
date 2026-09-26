# Konflate

Read-only rendered diffs for pull requests against `master`. The public
repository needs no GitHub token to fetch PRs. Konflate cannot post checks or
comments; the GitHub Actions `Flate` check still validates automatic updates.

```bash
kubectl --context admin@homelab -n konflate port-forward svc/konflate 8080:8080
```

Open `http://localhost:8080` for the UI, or query
`http://localhost:8080/api/prs/<number>/summary`. The read-only MCP endpoint
is at `http://localhost:8080/mcp`.

Fork PRs are excluded from rendering. Source fetches reject private and
loopback addresses. The in-memory cache is rebuilt after a pod restart.
