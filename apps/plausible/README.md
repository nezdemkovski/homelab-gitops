# Plausible

Flux installs the pinned `plausible-analytics` chart as release `plausible` in
the existing `plausible` namespace. Keeping the release name, namespace,
fullname overrides, chart version, and storage values unchanged preserves these
StatefulSet claim names during the Argo to Flux handoff:

- `data-plausible-postgresql-0`
- `data-plausible-clickhouse-shard0-0`

The HelmRelease deliberately allows Helm to take ownership of the resources
that Argo originally rendered. Do not reconcile it while the Argo application
still has automated sync, pruning, or its resource finalizer enabled.

## Cutover requirements

Before reconciling Flux:

1. Stop writes by scaling the Plausible Deployment to zero after disabling
   Argo self-heal.
2. Record PostgreSQL row counts and ClickHouse table/part counts.
3. Create a PostgreSQL custom-format logical dump with `pg_dump`.
4. Stop both database StatefulSets and archive both PVC contents while they are
   quiescent. This cluster has no CSI VolumeSnapshot support, so a cold PVC copy
   is the recovery boundary for ClickHouse.
5. Record SHA-256 hashes for the dump and both archives, and store the copies
   outside the Talos node before changing GitOps ownership.
6. Remove automated sync and the Argo Application finalizer, then delete the
   orphaned Argo Application without deleting the namespace, workloads,
   Secrets, PVCs, or PVs.
7. Reconcile `plausible`, then `plausible-reader` through Flux.

Both current PVs use `Retain`. Keep them until the public endpoint, database
counts, and Grafana read-only queries have all been verified after cutover.

## Verification

- Flux source, HelmRelease, and both Kustomizations are Ready.
- The PostgreSQL and ClickHouse PVC names and bound PV IDs are unchanged.
- PostgreSQL `pg_database_size`, table counts, and selected row counts match the
  stopped-write baseline.
- ClickHouse active part rows/bytes and per-table row counts match the baseline.
- `grafana_reader` retains `SELECT` and `dictGet` grants.
- All three Plausible pods are Ready with the pinned images.
- `https://analytics.nezdemkovski.cloud/` returns HTTP 200 and recent events are
  visible in both Plausible and Grafana.
