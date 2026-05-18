# n8n

n8n is installed by Argo CD from the official OCI Helm chart:

```text
ghcr.io/n8n-io/n8n-helm-chart/n8n
```

The chart version is pinned in `application.yaml` as `targetRevision`.

## Mode

This deployment uses standalone mode:

```text
queueMode.enabled=false
database.type=sqlite
persistence.storageClassName=local-path
```

SQLite data is stored in a PVC backed by the local-path provisioner. This is
fine for homelab experiments, but it is not HA. Moving to queue mode later
requires PostgreSQL and Redis.

## Secret

The chart expects an existing Kubernetes Secret named `n8n-env` in the `n8n`
namespace. It is created manually for now and must not be committed to git.

Required keys:

```text
N8N_ENCRYPTION_KEY
N8N_HOST
N8N_PORT
N8N_PROTOCOL
```

The encryption key protects stored n8n credentials. Losing or changing it can
make existing workflow credentials unreadable.

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
