# Supabase

Supabase is installed by Argo CD from the community Kubernetes Helm chart:

```text
https://supabase-community.github.io/supabase-kubernetes
```

The chart and all enabled container images are pinned in `application.yaml`.
The deployment intentionally keeps the chart's Kong gateway because chart
`0.7.2` does not yet use the newer Envoy-based self-hosting layout.

## Public endpoint

Cloudflare Tunnel sends `supabase.nezdemkovski.cloud` to the in-cluster Kong
service. Kong exposes the Supabase APIs and protects Studio at `/` with HTTP
basic authentication. PostgreSQL is not published outside the cluster.

## Secrets

Runtime credentials are stored in the Homelab 1Password vault. External
Secrets Operator syncs them into `supabase/supabase-secrets`. No credential
values belong in Git.

## Storage

PostgreSQL, Storage, Edge Functions, Studio snippets, the Deno cache, and the
pgsodium state use `local-path` PVCs. PVCs are marked `Prune=false`; the
underlying volumes are still node-bound and require database-aware backups.

Image transformation, Analytics, Vector, and MinIO are disabled for the first
deployment. Storage uses its persistent filesystem backend.

## Authentication

Email signup is enabled with automatic confirmation. SMTP delivery is not yet
configured, so recovery and other outbound emails will not work until real
SMTP settings are added.

## Verification

After Argo reports `Synced/Healthy`, verify all pods and PVCs, the ExternalSecret
condition, the Kong endpoint, the REST API response, Studio basic auth, and a
real PostgreSQL query before treating the deployment as complete.
