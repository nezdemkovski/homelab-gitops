# Grafana MCP

Internal MCP server for Grafana.

This service is intentionally not exposed through Cloudflare Tunnel yet. It is
available only inside the cluster as:

```text
grafana-mcp.grafana-mcp.svc.cluster.local:8000
```

1Password item:

- `Homelab/grafana-mcp` - Grafana service account token.

The Grafana service account is named `grafana-mcp` and currently uses the
`Admin` role so MCP clients can create and update dashboards.
