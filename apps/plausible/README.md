# Plausible

Flux installs `plausible-analytics` as release `plausible` in the
`plausible` namespace. The stable release name, namespace, fullname overrides,
and storage values preserve these StatefulSet claims:

- `data-plausible-postgresql-0`
- `data-plausible-clickhouse-shard0-0`

Before a chart or storage migration, stop writes, record PostgreSQL and
ClickHouse counts, create a PostgreSQL custom-format dump, and cold-copy both
PVCs outside the cluster node. This cluster has no CSI VolumeSnapshot support,
so the cold ClickHouse copy is the recovery boundary.

After reconciliation, verify the original PVC/PV identities, database counts,
ClickHouse parts, `grafana_reader` grants, pod readiness, the public analytics
endpoint, and recent events in both Plausible and Grafana.
