# Monitoring

Shared monitoring stack for the homelab cluster.

Grafana is exposed through the Cloudflare Tunnel at:

```text
grafana.nezdemkovski.cloud
```

Prometheus is intentionally internal-only. It is used as a Grafana datasource
and is not exposed through Cloudflare.

Internal endpoints:

```text
grafana.monitoring.svc.cluster.local:80
grafana-mcp.monitoring.svc.cluster.local:8000
prometheus-prometheus.monitoring.svc.cluster.local:9090
```

1Password items:

- `Homelab/grafana` - Grafana admin login.
- `Homelab/grafana-mcp` - Grafana service account token for MCP.
- `Homelab/nezdemos-grafana-reader` - read-only Postgres role for NezdemOS
  dashboards.

Grafana UI users live in Grafana's own database on the PVC. They are not
managed from 1Password/GitOps.
