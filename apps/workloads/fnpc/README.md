# FNPC

Financial Nonsense Prevention Committee runs from the published OCI Helm chart:

```text
oci://ghcr.io/nezdemkovski/charts/fnpc
```

The public service and Telegram webhook are routed through Cloudflare Tunnel.

Runtime secrets live in 1Password:

```text
Homelab/fnpc
Homelab/fnpc-postgres
Homelab/fnpc-clickhouse
Homelab/Ynab
```

Postgres is owned by homelab GitOps manifests in this directory. The FNPC chart
only consumes the externally managed Postgres service and owner Secret.

Mastra observability is written to a dedicated `fnpc-clickhouse` StatefulSet and
PVC in the `fnpc` namespace. Its internal system logs and profilers are disabled
by the application chart, and observability tables retain 14 days of data.
