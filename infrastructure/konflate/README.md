# Konflate

Read-only rendered diffs for pull requests against `master`. The public
repository needs no GitHub token to fetch PRs. Konflate cannot post checks or
comments; the GitHub Actions `Flate` check still validates automatic updates.

```bash
kubectl --context admin@homelab -n konflate port-forward svc/konflate 18080:8080
```

Open `http://localhost:18080` for the UI, or query
`http://localhost:18080/api/prs/<number>/summary`. The read-only MCP endpoint
is at `http://localhost:18080/mcp`.

Fork PRs are excluded from rendering. Source fetches reject private and
loopback addresses. The in-memory cache is rebuilt after a pod restart.
Private OCI sources whose credentials live only in cluster Secrets are skipped
during offline rendering, so review those updates separately.
