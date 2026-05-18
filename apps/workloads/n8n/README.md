# n8n

n8n is installed by Argo CD from the official OCI Helm chart:

```text
ghcr.io/n8n-io/n8n-helm-chart/n8n
```

The chart version is pinned in `application.yaml` as `targetRevision`. The n8n
container image tag is pinned separately under `image.tag`; do not rely on the
chart default `stable` image tag.

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
