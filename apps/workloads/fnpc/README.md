# FNPC

Financial Nonsense Prevention Committee runs from the published OCI Helm chart:

```text
oci://ghcr.io/nezdemkovski/charts/fnpc
```

The Telegram bot uses polling, so it does not need public ingress.

Runtime secrets live in 1Password:

```text
Homelab/fnpc
Homelab/fnpc-postgres
Homelab/fnpc-clickhouse
```

The chart deploys CloudNativePG Postgres for Mastra and financial state.
Mastra observability is written to a dedicated `fnpc-clickhouse` StatefulSet and
PVC in the `fnpc` namespace.
