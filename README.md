# Homelab GitOps

The active cluster configuration is reconciled by Flux from the `master` branch at `clusters/homelab`.

Argo CD and its former `apps/` tree were retired after the Flux migration. Their
history remains available in Git.

## Bootstrap

Flux is bootstrapped with its CLI against the canonical branch and cluster path:

```bash
flux bootstrap github \
  --owner=nezdemkovski \
  --repository=homelab-gitops \
  --branch=master \
  --path=clusters/homelab \
  --personal
```

Application and infrastructure manifests now live on the `master` branch.
