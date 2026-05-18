# NocoDB

NocoDB is currently disabled. Its Kubernetes manifests are kept in `_disabled/`
so the root Argo CD application ignores them.

NocoDB runs from plain Kubernetes manifests using the official image:

```text
nocodb/nocodb:2026.04.5
```

The image tag is pinned in `deployment.yaml`.

## Storage

NocoDB metadata is stored in a dedicated PostgreSQL StatefulSet:

```text
nocodb/nocodb-postgres
```

PostgreSQL data and local NocoDB app data are stored on PVCs backed by the
local-path provisioner. This is fine for homelab experiments, but it is not HA.

## Secrets

The source of truth is the `nocodb` item in the `Homelab` 1Password vault.
External Secrets Operator syncs it into Kubernetes.

Required keys:

```text
POSTGRES_DB
POSTGRES_USER
POSTGRES_PASSWORD
NC_DB
NC_AUTH_JWT_SECRET
NC_CONNECTION_ENCRYPT_KEY
NC_PUBLIC_URL
```

Do not rotate `NC_AUTH_JWT_SECRET` or `NC_CONNECTION_ENCRYPT_KEY` unless NocoDB
data is intentionally migrated.

Public access goes through Cloudflare Tunnel. The public hostname is stored in
1Password and Cloudflare DNS, not in Git.
