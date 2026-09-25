# Monitoring Flux handoff

This directory declares the existing `monitoring` release for Flux. The local
chart remains in `charts/monitoring`, with dependency versions pinned by
`Chart.lock`.

The handoff is designed to adopt the existing release names and storage:

- Grafana uses PVC `grafana` at `/var/lib/grafana`.
- Prometheus uses the operator-managed PVC whose name starts with
  `prometheus-prometheus-prometheus-db-prometheus-prometheus-prometheus-0`,
  mounted at `/prometheus/prometheus-db` on the volume and `/prometheus` in the
  container.
- Helm stores the new release metadata in the `monitoring` namespace.

## Cutover checklist

Do not reconcile `clusters/homelab/monitoring.yaml` while the Argo CD
`monitoring` Application still has automated sync or its resource finalizer.

1. Record the Grafana database integrity, user/dashboard counts, Prometheus
   TSDB head statistics and the two PVC/PV bindings.
2. Disable Argo CD automated sync and remove only the Application resource
   finalizer. Confirm Argo no longer self-heals the release.
3. Stop Grafana and Prometheus, then make cold backups of both PVCs. For
   Grafana, copy the whole PVC and run `PRAGMA integrity_check` against the
   copied `grafana.db`. For Prometheus, copy the full TSDB including WAL and
   verify that `promtool tsdb analyze` can read the copy.
4. Keep the original PV reclaim policies set to `Retain`. Record the exact PV
   names before any controller handoff.
5. Reconcile the Flux `monitoring` Kustomization. Its Helm install takes
   ownership of existing chart resources and keeps the canonical resource,
   service and PVC names.
6. Verify both original PVC UIDs and PV names are unchanged before starting
   workloads. If either binding changed, suspend Flux and restore the cold
   backup instead of accepting an empty volume.
7. Verify Grafana database integrity and counts, Grafana API health, Prometheus
   TSDB time range and series counts, scrape targets, dashboards, datasources,
   MCP access and the public Grafana endpoint.
8. Delete the Argo CD Application manifest only after Flux is Ready and all
   data checks pass. Keep the cold backups until a later explicit cleanup.

Rollback before deleting the Argo manifest is to suspend the Flux
Kustomization, remove the Flux Helm release metadata without deleting the
workloads or PVCs, restore Argo ownership, and re-enable Argo automated sync.
