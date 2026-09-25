# Monitoring Chart

Umbrella chart for the homelab monitoring stack.

It deploys:

- Grafana, exposed at `grafana.nezdemkovski.cloud`.
- Grafana MCP, exposed only on the home LAN through NodePort `30800`.
- kube-prometheus-stack with internal Prometheus, Prometheus Operator,
  kube-state-metrics, and node-exporter.
- GitOps-provisioned Grafana datasources and dashboards.

Prometheus is internal-only and should not get a public hostname. Use Grafana
for normal browsing, or `kubectl port-forward` for one-off Prometheus debugging.

## Analytics

Grafana also provisions a read-only `Plausible ClickHouse` datasource and a
`Plausible Analytics` dashboard under the Analytics folder. This dashboard is
shaped for quick AI inspection through Grafana MCP: traffic, events, top pages,
referrers, countries, devices, UTM campaigns, and recent activity.
