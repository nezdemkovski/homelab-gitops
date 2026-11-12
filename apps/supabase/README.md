# Supabase

The operator and project charts are pinned to `0.8.4`. Flux installs the operator
from `infrastructure/supabase-operator` and the project from `apps/supabase/project`.
The legacy `supabase` chart `0.8.0` remains installed during the migration, and
Cloudflare Tunnel still sends `https://supabase.nezdemkovski.cloud` to its Kong
service. The new Envoy gateway is currently private to the cluster.

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

`supabase-db-recovery-20261112` retains the pre-migration physical database,
checksums, aggregate verification metadata, and pgsodium configuration. It is a
node-local recovery copy, not an off-node backup. Original application PVCs and
older Released PVs are retained. Namespace, recovery PVC, and stateful project
resources have prune protection; local-path volumes use `Retain` and remain
bound to this node.

A synthetic row survived recreation of `supabase-postgres-0` and was readable
through both the original anon API key and the new publishable key. PostgreSQL's
data path resolves to the persistent XFS filesystem. The temporary probe table
is removed after testing.

## Credentials and cutover

Existing database, dashboard, Realtime, Meta, and Storage credentials are merged
from the `supabase` item in the Homelab 1Password vault into operator-owned
Secrets. Merge targets are checked for `SecretSynced`, including on bootstrap.
The original JWT secret and legacy anon/service-role API keys have also been
preserved in the new project's JWT Secret, including its HMAC JWK entries.

**Cutover is pending:** seven new operator-generated key fields still need to be
saved in that same 1Password item and mapped through External Secrets. Connect
can read this item but rejects writes with HTTP 403. Until personal 1Password
CLI access is available, do not publish the new gateway or remove the legacy
release. New generated keys currently exist only in the operator's Kubernetes
Secrets; ordinary operator reconciliation preserves them.

After key storage and fresh ExternalSecret verification, recheck the legacy
application for writes, switch the tunnel backend to `supabase-envoy`, verify
the public API and Studio, and only then remove the legacy HelmRelease. Keep
its PVCs and the recovery copy until explicitly retired.

The private gateway has passed Auth, REST table reads, Storage status, Meta
health, Studio authentication, and public-only JWKS checks with the original
credentials. Envoy intentionally restricts the REST OpenAPI root to service-role
keys. Analytics, Vector, Supavisor, and MinIO are disabled; imgproxy is enabled
with Storage. Email confirmation remains automatic and SMTP remains unconfigured.
