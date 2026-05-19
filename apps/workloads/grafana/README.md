# Grafana

Shared dashboarding UI for homelab services.

Grafana is exposed through the Cloudflare Tunnel and keeps credentials in
1Password.

1Password items:

- `Homelab/grafana` - Grafana admin login.
- `Homelab/nezdemos-grafana-reader` - read-only Postgres role for NezdemOS
  dashboards.

The NezdemOS Postgres datasource is provisioned from GitOps. Database grants
are owned by the `nezdemos` chart because the database belongs to that stack.
