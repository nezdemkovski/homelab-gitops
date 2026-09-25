# Auth Argo-to-Flux handoff

This directory prepares the existing `auth` namespace for a staged ownership
handoff. Both cluster Kustomizations are committed with `spec.suspend: true`.
They must stay suspended until the live-state checks and backups below pass.

## Data boundaries

- `auth-postgres` is an existing CloudNativePG cluster. Its PVC must be adopted
  in place; never delete or recreate the `Cluster`, namespace, or PVC during the
  controller handoff.
- `auth-rustfs` is an existing chart-managed PVC. The HelmRelease explicitly
  enables Helm ownership takeover so the claim is adopted in place.
- Redis is configured as an ephemeral cache with RDB and AOF persistence
  disabled. Record `DBSIZE` immediately before cutover. If it is non-zero,
  export an RDB backup before replacing the Redis pod.
- Runtime credentials continue to come from the existing 1Password-backed
  ExternalSecrets. Do not copy Secret values into Git or migration logs.

## Required preflight

1. Confirm Argo is healthy on chart `0.2.49` and record the live workload image
   digests, PVC names, PV names, reclaim policies, ExternalSecret conditions,
   and public realm discovery responses.
2. Record PostgreSQL database size, schema/table counts, and a checksum of a
   logical `pg_dump`. Restore the dump into a disposable database and compare
   schema/table counts before continuing.
3. Create a uniquely named manual CloudNativePG `Backup` and wait for phase
   `completed`. Record its start/stop time and `firstRecoverabilityPoint`.
4. Quiesce API writes, archive the complete RustFS `/data` tree, and record a
   sorted per-file checksum manifest. Keep the archive outside the cluster.
5. Confirm both bound PVs still use `Retain`. Abort if either expected claim is
   absent, unbound, newly provisioned, or attached to a different node.

## Handoff sequence

1. In the Argo branch, add `argocd.argoproj.io/sync-options: Prune=false` to
   the namespace, both infrastructure ExternalSecrets, the CNPG Cluster, and
   ScheduledBackup. Sync `homelab-root` and verify those guards are live before
   removing any Auth infrastructure manifest from that branch. The root Argo
   Application has automated prune enabled, so skipping this phase can delete
   infrastructure even after Flux has adopted it.
2. Disable Argo automated sync for the child `auth` Application, remove its
   resources finalizer, and verify that all chart resources remain running after
   the Application is orphaned.
3. Unsuspend only `auth-infra`. Wait for the Flux Kustomization, ExternalSecrets,
   CNPG Cluster, and ScheduledBackup to report Ready. Verify the PostgreSQL pod
   UID and PVC/PV identity did not change.
4. Stop write traffic briefly and record a final PostgreSQL/RustFS/Redis
   baseline. Unsuspend `auth`; its dependency keeps the HelmRelease behind the
   ready infrastructure layer.
5. Wait for the OCIRepository and HelmRelease to become Ready. The release name,
   namespace, service names, chart version, values, and image digests are kept
   identical to the Argo deployment.
6. Verify PostgreSQL row counts and realm schemas, RustFS file checksums, public
   OpenID discovery for every active realm, login/admin flows, and dependent
   applications before restoring normal traffic.
7. Remove the Argo manifests only after the Flux-managed service has completed
   a soak period. Once Argo no longer desires the guarded resources, remove its
   tracking and prune annotations, then confirm Flux still reports them Ready.
   Keep both backups until a later cleanup window.

Never enable Argo self-heal while either Flux Kustomization is active. Never
delete the HelmRelease as a rollback action because Helm uninstall may remove
chart-managed resources, including the RustFS PVC.

## Rollback

1. Suspend `auth` and `auth-infra`; leave their resources and HelmRelease in the
   cluster.
2. If data is healthy, restore the Argo Application with automated sync still
   disabled, verify its diff, then let Argo adopt the existing resources.
3. If PostgreSQL or RustFS data is suspect, restore into new, separately named
   resources from the verified backups. Validate them before changing any
   Service or database endpoint.
4. Re-enable one controller only after the chosen owner reports healthy. Keep
   the other controller suspended throughout recovery.
