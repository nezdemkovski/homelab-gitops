# Forgejo

Forgejo is installed by Argo CD from the official OCI Helm chart:

```text
codeberg.org/forgejo-contrib/forgejo
```

The chart version is pinned in `application.yaml` as `targetRevision`. The
container image tag is pinned separately under `image.tag`.

## Storage

Forgejo uses a PVC backed by the local-path provisioner for `/data`.

The default database is SQLite. This is acceptable for a small single-user
homelab instance. Move to PostgreSQL before using it as a shared long-term forge
with several active users.

## Secrets

The admin credentials and public URL/domain settings are stored in 1Password:

```text
Homelab/forgejo
```

External Secrets Operator syncs them into:

```text
forgejo/forgejo-env
```

Public hostnames and Cloudflare Tunnel ingress rules are stored in 1Password,
not in Git.
