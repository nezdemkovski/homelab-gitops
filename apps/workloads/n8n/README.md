# n8n

n8n is installed by Argo CD from the local stack chart:

```text
charts/n8n-stack
```

The stack chart depends on the official `n8n` chart and the local
CloudNativePG cluster manifests in this directory. The upstream chart version is
pinned in `charts/n8n-stack/Chart.yaml`; the n8n container image tag is pinned
separately in `charts/n8n-stack/values.yaml`.

PostgreSQL is managed by CloudNativePG:

```text
n8n-postgres-cnpg
```

Applications should connect through the writable service:

```text
n8n-postgres-cnpg-rw.n8n.svc.cluster.local:5432
```

The active database PVC is `n8n-postgres-cnpg-1`. The old
`data-n8n-postgres-0` PVC is intentionally retained as a rollback copy after the
manual migration.

## Mode

This deployment uses standalone mode with PostgreSQL:

```text
queueMode.enabled=false
database.type=postgresdb
persistence.storageClassName=local-path
```

PostgreSQL data and `/home/node/.n8n` appdata are stored on PVCs backed by
local-path. CloudNativePG gives us a standard Postgres lifecycle, but this is
still not HA on a single-node cluster. Moving to queue mode later requires Redis.

## Secret

The chart expects an existing Kubernetes Secret named `n8n-env` in the `n8n`
namespace.

The source of truth is the `n8n` item in the `Homelab` 1Password vault. External
Secrets Operator reads that item through the `onepassword` `ClusterSecretStore`
and merges the values into the existing Kubernetes Secret.

Required keys:

```text
N8N_ENCRYPTION_KEY
N8N_HOST
N8N_PORT
N8N_PROTOCOL
WEBHOOK_URL
N8N_EDITOR_BASE_URL
DB_POSTGRESDB_DATABASE
DB_POSTGRESDB_USER
DB_POSTGRESDB_PASSWORD
DB_POSTGRESDB_PORT
DB_POSTGRESDB_SCHEMA
N8N_RUNNERS_AUTH_TOKEN
```

The encryption key protects stored n8n credentials. Losing or changing it can
make existing workflow credentials unreadable.

Public access goes through Cloudflare Tunnel. The public hostname is stored in
1Password and synced through `n8n-env`.

## Access

Open the UI with a local port-forward:

```bash
export KUBECONFIG=/Users/yuri/Sites/homelab-gitops/kubeconfig

kubectl -n n8n port-forward svc/n8n-main 5678:5678
```

Then open:

```text
http://localhost:5678
```
