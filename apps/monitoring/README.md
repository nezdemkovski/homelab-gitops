# Monitoring

Flux reconciles the local `charts/monitoring` chart. Dependency versions are
pinned in `Chart.lock`.

Persistent state:

- Grafana uses PVC `grafana` at `/var/lib/grafana`.
- Prometheus uses the operator-managed PVC whose name starts with
  `prometheus-prometheus-prometheus-db-prometheus-prometheus-prometheus-0`.
  `storageSpec.disableMountSubPath: true` and the permission init container
  both mount its root directly. Do not add `subPath` without verifying the
  Talos kubelet host bind mount: otherwise data can land in kubelet overlay.

Before changing chart storage values, StatefulSet identity, or release names,
record both PVC/PV bindings and take cold copies outside the cluster node. Check
the copied Grafana database with `PRAGMA integrity_check` and verify the copied
Prometheus TSDB with `promtool tsdb analyze`.

After reconciliation, confirm the original PVC UIDs and PV names, Grafana
database integrity and dashboard counts, Prometheus time range and series
counts, scrape targets, datasources, public Grafana access, and MCP access.

PVC identity and Ready status alone do not prove persistence. Verify the
Prometheus process mount filesystem is the node disk (`xfs`), not `overlay`;
read the same files through an independent read-only PVC mount, then query
pre-restart samples after recreating the Prometheus pod.
