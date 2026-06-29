# FNPC

FNPC is currently disabled. Its Argo CD application is kept as
`application.yaml.disabled`, and its raw Kubernetes manifests are kept in
`_disabled/` so the root Argo CD application ignores them.

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

Postgres is owned by homelab GitOps manifests in this directory. The FNPC chart
only consumes the externally managed Postgres service and owner Secret.

Mastra observability is written to a dedicated `fnpc-clickhouse` StatefulSet and
PVC in the `fnpc` namespace.
