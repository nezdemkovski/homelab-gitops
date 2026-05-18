# Homarr

Homarr is installed by Argo CD from the official OCI Helm chart:

```text
ghcr.io/homarr-labs/charts/homarr
```

The chart version is pinned in `application.yaml` as `targetRevision`. The
container image tag is pinned separately under `image.tag`.

## Storage

Homarr uses a PVC backed by the local-path provisioner for `/appdata`.

## Secrets

The `SECRET_ENCRYPTION_KEY` value is stored in 1Password:

```text
Homelab/homarr/SECRET_ENCRYPTION_KEY
```

External Secrets Operator syncs it into:

```text
homarr/homarr-env
```

Public hostnames and Cloudflare Tunnel ingress rules are stored in 1Password,
not in Git.

