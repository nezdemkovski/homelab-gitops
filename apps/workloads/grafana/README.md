# Grafana Stack

Shared dashboarding stack for homelab services.

Grafana is exposed through the Cloudflare Tunnel and keeps credentials in
1Password. The internal Grafana MCP server is deployed in the same stack and is
not exposed publicly.

Internal MCP endpoint:

```text
grafana-mcp.grafana.svc.cluster.local:8000
```

1Password items:

- `Homelab/grafana` - Grafana admin login.
- `Homelab/grafana-mcp` - Grafana service account token for MCP.
- `Homelab/nezdemos-grafana-reader` - read-only Postgres role for NezdemOS
  dashboards.

The NezdemOS Postgres datasource is provisioned from GitOps. Database grants
are owned by the `nezdemos` chart because the database belongs to that stack.
