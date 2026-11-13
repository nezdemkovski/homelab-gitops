# Supabase

The operator and project charts are pinned to `0.8.4`. Flux installs the operator
from `infrastructure/supabase-operator` and the project from `apps/supabase/project`.
Cloudflare Tunnel sends `https://supabase.nezdemkovski.cloud` to
`supabase-envoy.supabase.svc.cluster.local:8000`. The legacy `supabase` chart
`0.8.0`, its Kong gateway, and its ExternalSecret were retired on 2026-11-13.

## Storage

The original PostgreSQL data was written through a `subPath` mount into kubelet's
temporary filesystem. The Talos kubelet now has a shared bind mount of
`/var/lib/local-path-provisioner`; its machine patch and application instructions
are in `infrastructure/local-path-provisioner/`. The legacy chart also mounts its
PostgreSQL PVC directly and shuts down PostgreSQL as the correct Unix user.

The database and pgsodium configuration were copied inside the cluster, with
per-file checksums and an isolated PostgreSQL restore check. The operator's
`supabase-postgres-data` PVC contains the preserved database and pgsodium key.
The PostgreSQL image remains `supabase/postgres:17.6.1.136` for this migration.
The initial Project bootstrap migration is disabled because the imported
`_supabase` database already exists; component migrations remain enabled.

The recovery PVC, six legacy application PVCs, and six older Released PVs were
permanently removed on 2026-11-13 at the owner's request after verification.
The local-path provisioner deleted all 13 corresponding directories. Only the
three active PVCs remain: `supabase-postgres-data`, `supabase-storage-data`, and
`supabase-studio-data`. Their PV reclaim policies remain `Retain`; these volumes
are node-bound. No migration recovery copy remains.

A synthetic row survived recreation of `supabase-postgres-0` and was readable
through both the original anon API key and the new publishable key. PostgreSQL's
data path resolves to the persistent XFS filesystem. The temporary probe table
is removed after testing.

## Credentials and cutover

Database, dashboard, Realtime, Meta, Storage, JWT, asymmetric signing, opaque
API, and vault encryption credentials are restored from the `supabase` Secure
Note in the Homelab 1Password vault into five operator-owned Secrets through
External Secrets with `creationPolicy: Merge`. Bootstrap health requires
`SecretSynced`, rather than treating a missing merge target as healthy.

The original database password, JWT secret, anon/service-role API keys,
dashboard login, and crypto keys were preserved. The seven additional operator
key fields were written to 1Password and read back; all prior values were
verified unchanged. Fresh ESO sync preserved all five Secret data hashes.
Database connection metadata in the same item now points to `supabase-postgres`.
No generated Secret manifests, key material, or database exports were committed.

Before public cutover, both old and new databases still had zero users, Storage
objects, and public application tables. The new gateway passed public HTTPS
checks before the legacy HelmRelease was removed. Legacy disks were initially
retained, then deleted separately on the owner's explicit cleanup request. The
namespace and three active application disks were preserved.

Private API checks included REST table reads. Public HTTPS checks passed for
Auth, service-role REST OpenAPI, Storage status, Meta health, Studio
authentication, and public-only JWKS with the original credentials. Envoy intentionally restricts the REST OpenAPI root to service-role
keys. Analytics, Vector, Supavisor, and MinIO are disabled; imgproxy is enabled
with Storage. Email confirmation remains automatic and SMTP remains unconfigured.
