# Plausible

Plausible is installed by Argo CD from the `imio/plausible-analytics` Helm chart:

```text
https://imio.github.io/helm-charts
```

The chart version is pinned in `application.yaml` as `targetRevision`. The
container image tag is pinned separately under `image.tag`.

## Storage

This deployment uses the bundled PostgreSQL and ClickHouse charts with
`local-path` PVCs:

```text
plausible-postgresql  5Gi
plausible-clickhouse  10Gi
```

## Secrets

Runtime secrets, database passwords, and the public base URL are stored in
1Password:

```text
Homelab/plausible
```

External Secrets Operator syncs them into:

```text
plausible/plausible-env
```

Grafana uses a separate read-only ClickHouse user, also sourced from
`Homelab/plausible`. Argo CD keeps that user idempotently configured with the
`plausible-clickhouse-grafana-reader` PostSync job.

Public hostnames and Cloudflare Tunnel ingress rules are stored in 1Password,
not in Git.

## Initial Setup

Registration is enabled for the first account creation. Disable it in
`application.yaml` after the first user exists.
