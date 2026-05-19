# Grafana Stack

Shared dashboarding stack for homelab services.

The stack contains Grafana and the internal Grafana MCP server. Grafana is
exposed through the Cloudflare Tunnel at `grafana.nezdemkovski.cloud`; MCP stays
cluster-internal at `grafana-mcp.grafana.svc.cluster.local:8000`.

1Password items:

- `Homelab/grafana-mcp` - Grafana service account token for MCP.
- `Homelab/nezdemos-grafana-reader` - read-only Postgres role for NezdemOS
  dashboards.

Grafana UI users live in Grafana's own database on the PVC. They are not managed
from 1Password/GitOps.

Database grants are owned by the `nezdemos` chart because the database belongs
to that stack.
