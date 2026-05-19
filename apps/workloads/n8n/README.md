# n8n

n8n is installed by Argo CD from the local stack chart:

```text
charts/n8n-stack
```

The stack chart depends on the official `n8n` chart and the local
`n8n-postgres` chart. The upstream chart version is pinned in
`charts/n8n-stack/Chart.yaml`; the n8n container image tag is pinned separately
in `charts/n8n-stack/values.yaml`.

PostgreSQL is managed by the local chart:

```text
charts/n8n-postgres
```

The local chart keeps the existing `StatefulSet`, `Service`, `ExternalSecret`,
and PVC naming stable. The database PVC is `data-n8n-postgres-0`.

## Mode

This deployment uses standalone mode with PostgreSQL:

```text
queueMode.enabled=false
database.type=postgresdb
persistence.storageClassName=local-path
```

PostgreSQL data and `/home/node/.n8n` appdata are stored on PVCs backed by the
local-path provisioner. This is fine for homelab experiments, but it is not HA.
Moving to queue mode later requires Redis.

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
```

The encryption key protects stored n8n credentials. Losing or changing it can
make existing workflow credentials unreadable.

Public access goes through Cloudflare Tunnel. The public hostname is stored in
1Password and synced through `n8n-env`.

## Access

Open the UI with a local port-forward:

```bash
export KUBECONFIG=/Users/yuri/Sites/homelab-gitops/kubeconfig

kubectl -n n8n port-forward svc/n8n 5678:5678
```

Then open:

```text
http://localhost:5678
```
