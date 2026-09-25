# Homelab GitOps

The active cluster configuration is reconciled by Flux from the `flux-gitops`
branch at `clusters/homelab`.

Argo CD and its former `apps/` tree were retired after the Flux migration. Their
history remains available in Git.

## Bootstrap

Flux was bootstrapped with its CLI against the dedicated branch and canonical
cluster path:

```bash
flux bootstrap github \
  --owner=nezdemkovski \
  --repository=homelab-gitops \
  --branch=flux-gitops \
  --path=clusters/homelab \
  --personal
```

Application and infrastructure manifests now live on the `flux-gitops` branch.
