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

Grafana MCP caller authentication uses `Homelab/grafana/MCP_SERVER_TOKEN`,
separate from the Grafana service-account `token` field. External Secrets creates
`monitoring/grafana-mcp-server-token`; the chart does not generate its own caller
credential. Preserve this value when reorganizing secrets.

Codex and Cursor can share the local stdio bridge:

```bash
install -m 700 scripts/grafana-mcp-remote.sh ~/.codex/bin/grafana-mcp-remote.sh
```

The bridge uses global `~/.kube/config` with `admin@homelab`, forwards only on
localhost, and reads the caller token at startup. Its temporary header file has
owner-only permissions and is removed when the bridge exits. Tokens are not
embedded in client configuration or process arguments.
The bridge selects a free loopback port in `18080–18111`. Those exact hosts are
allowed by the server; arbitrary Host headers and browser Origins remain denied.

## Flux monitoring

`flux-system` PodMonitor scrapes the four installed Flux controllers on their
`http-prom` port every 30 seconds. A service-specific egress rule allows only
Prometheus to reach those pods on TCP 8080; Flux's bootstrap `allow-scraping`
policy already permits the matching ingress.

The existing kube-state-metrics also exports `gotk_resource_info` for
Kustomization, HelmRelease and source resources, with list/watch permissions
restricted to those resource types. Its standard Kubernetes collectors remain
enabled for the existing cluster dashboards.

The Flux folder provisions **Flux Cluster Stats** and **Flux Control Plane**.
Dashboard JSON and custom-resource metric mappings are adapted from
[fluxcd/flux2-monitoring-example](https://github.com/fluxcd/flux2-monitoring-example/tree/7ab65dc8b90f7a6751d88f18bbb4e1bee33bf334)
at commit `7ab65dc8b90f7a6751d88f18bbb4e1bee33bf334`; see
[dashboards/flux-LICENSE](dashboards/flux-LICENSE). Local adaptations pin the
Prometheus UID, set namespace defaults, retain core collectors and render zero
for healthy failing-resource stat panels. Empty Bucket/error series are normal
when the cluster has no corresponding resources or events.
