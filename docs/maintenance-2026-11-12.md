# Homelab maintenance — 2026-11-12

This is a verified maintenance snapshot, not a substitute for checking live state.

## Versions

| Component | Before | After |
| --- | --- | --- |
| Kubernetes | 1.36.0 | 1.36.6 |
| Talos OS | 1.14.2 | 1.14.6 |
| etcd | 3.7.1 | 3.7.3 |
| Flux | 2.9.6 | 2.10.0 |
| n8n main and runners | 2.48.2 | 3.2.0 |
| Paperclip | 2026.1012.0 | 2026.1106.0 |
| kube-prometheus-stack chart | 92.11.0 | 93.2.2 |
| Prometheus | 3.15.0 | 3.16.0 |
| Prometheus Operator | 0.94.1 | 0.95.2 |
| Grafana | 13.2.4 | 13.3.1 |
| Grafana MCP | 2.1.1 | 2.3.0 |
| Forgejo chart | 17.3.1 | 17.3.2 |

Forgejo's application image remains `17.0.1-rootless`. Its OCI chart now comes
from the official `code.forgejo.org/forgejo-helm/forgejo` registry. The old
Codeberg endpoint returned 403 and repeatedly failed Flux health checks.

The full Flux bundle updates controllers, CRDs and RBAC together. Provider and
Alert manifests now use the supported notification API v1. Superseded individual
controller and monitoring PRs were closed; accepted PRs were merged with rebase.

## Data and compatibility checks

- n8n database migrations passed on a restored NAS backup. All 49 retained node
  type/version pairs, including the installed Telegram community node, loaded in
  3.2.0. At the owner's request, six retired OpenAI v1 nodes and their connections
  were removed from two inactive workflows through the official import CLI.
  All ten workflows and seven credentials remain; no workflows were activated.
- Paperclip's 69 pending migrations passed on a restored database using the new
  production runtime bundle. Production retained one company, four agents,
  six issues and twenty heartbeat runs. Workspace cleanup keeps the previous
  seven-day cooldown; the newly introduced file compaction is disabled.
- Thataway's WAL archive now uses a PostgreSQL-system-specific prefix. The old
  archive was preserved, accumulated WAL was archived, and a fresh NAS backup
  restored successfully with PostGIS and matching place/tile/art counts.
  Three original released Swift model versions decoded live health, places and
  validation-error responses after maintenance.
- Grafana's SQLite backup was uploaded to
  `s3://cnpg-backups/maintenance/20261112/grafana-before-upgrade-db.tar.gz`.
  A downloaded copy passed SHA256, SQLite integrity and row-count checks.
  SHA256: `8c06c25adb458ee9eb24e4409d1547f13ca8ee7f4ae9bec5acf571c55bac3103`.

Additional completed PostgreSQL backups immediately before application changes:

| Database | Backup ID | Completed UTC |
| --- | --- | --- |
| n8n | 20261112T190512 | 19:05:17 |
| Paperclip | 20261112T191533 | 19:15:43 |
| Thataway | 20261112T185210 | 18:52:27 |

Temporary restore clusters, PVCs/PVs and backup helpers were removed after
verification. Production PVC bindings and Retain policies were preserved.

## MCP clients

The new chart enables caller authentication. The existing caller token was
preserved in `Homelab/grafana/MCP_SERVER_TOKEN` and is supplied through External
Secrets. The existing Grafana service-account `token` field is unchanged.

Codex and Cursor's shared bridge was updated from the obsolete repository-local
kubeconfig to global `admin@homelab`. It uses protected temporary header files,
explicit loopback ports and the existing authenticated SSE transport. A real
stdio test passed initialize, discovery of 80 tools and a Prometheus query;
no caller token appeared in logs. See the [monitoring README](../charts/monitoring/README.md).

## Verified state and owner choices

28 Kustomizations, 24 HelmReleases and 43 ExternalSecrets were Ready; all nine
production CloudNativePG clusters and application pods were ready. Public
Forgejo, n8n, Paperclip, Grafana, Thataway and Playdamnit API checks succeeded;
Uptime Kuma and Homarr returned their expected authentication redirects.

Prometheus reported no down targets. Node exporter exposed 49 collector status
series; six reported no data (`bcachefs`, `infiniband`, `kernel_hung`, `nfsd`,
`tapestats`, `zfs`), with no collector errors in its logs. Upstream deliberately
[uses the same zero status for no data and errors](https://github.com/prometheus/node_exporter/blob/v1.12.1/collector/collector.go#L147-L164);
these statuses alone do not establish a scrape failure. No collectors or
security controls were disabled.

VM 107 backup is intentionally excluded from the existing Proxmox schedules.
The ad-hoc backup was stopped at the owner's request, its leftover backup lock
was cleared, and schedules were not changed. No successful new VM backup is
claimed. The preflight storage check showed approximately 97% physical usage
and zero non-reserved available space on Proxmox `data`; no unrelated storage
or VM files were removed.

Kubernetes and Talos recovery contexts are in the global 0600 client configs.
Pre-maintenance etcd snapshots were saved off-node on the Mac in the protected
`/tmp/homelab-recovery` directory; they do not cover application volumes.

## Follow-up: metric history persistence

The later history check found that Prometheus had no retained samples before
2026-11-12 19:51:50 Europe/Prague, despite its 14-day / 8 GiB retention. The
original PVC UID was unchanged, but this was insufficient evidence of data
persistence. Its `prometheus-db` subPath resolved inside the Talos kubelet
overlay because `/var/lib/local-path-provisioner` was not bind-mounted into
kubelet. A direct read-only mount of the same PVC was empty; Prometheus
process mountinfo confirmed `overlay`. The configuration predates this update;
the first historical loss time is unknown. Older overlay snapshots inspected
did not contain another TSDB. Grafana itself mounts its PVC directly, and its
five provisioned dashboards remain available.

Prometheus was stopped gracefully, its current TSDB copied off-node to the Mac
with mode 0600 at
`/tmp/homelab-recovery/prometheus-before-persistence-fix-20261112.tar.gz`
(SHA256 `92410b2e293340dcec0b7ee5aa62fee9ee46612c84d41da40ea49716913d4e8c`).
The archive was restored onto the empty original PVC and all five regular
file hashes matched. `storageSpec.disableMountSubPath: true` and a matching
root mount in the permission init container were deployed from Git.

After deployment and an additional real pod recreation, WAL replay succeeded,
the original earliest timestamp and a pre-transfer historical query remained
available, and no Prometheus targets were down. Independent PVC inspection
found the restored files, and process mountinfo now shows XFS `/dev/sda6`.
Both Flux resources were resumed, Admin API remains disabled, and temporary
pods were removed. Earlier missing history was not recovered.

A separate audit also found Supabase PostgreSQL's `postgres-data` subPath on
the same kubelet overlay. No Supabase data or mounts were changed in this
monitoring repair; its persistence needs a separate database maintenance operation.

## Follow-up: dashboard query audit

Grafana MCP was used to execute every retained panel query through Grafana's
`/api/ds/query`, including actual datasource backend execution, response status,
frame fields, time types, row counts and nulls. The remaining dashboards contain
53 panels / 54 targets: Cluster Overview (11), Cluster Diagnostics (27 / 28),
and Plausible Analytics (15). Plausible's host-options SQL returned two sites;
its panel queries were checked with All and each host individually.

Fixes applied:

- Removed both WHOOP dashboards, their provider/mounts, retired NezdemOS
  datasource and unused reader-secret mapping after the owner confirmed WHOOP
  is no longer needed. No WHOOP database or 1Password item was deleted.
- Expanded the CNPG PodMonitor and only the required TCP 9187 network rules
  from three existing clusters to all nine production CNPG clusters. Verified
  one collector per namespace and successful database-size queries.
- Changed four diagnostic stat queries to boolean aggregation, so healthy
  sources return zero instead of an empty result. They still return no data
  when the underlying metric is absent. Filtered problem tables remain empty
  when no corresponding issue exists.
- Corrected session aggregates to use `sign` in Plausible's
  `VersionedCollapsingMergeTree` table. The live sample contained 45 rows and
  zero cancellation rows, so current totals agreed; the queries now also handle
  unmerged cancellation rows correctly, following the
  [ClickHouse engine semantics](https://clickhouse.com/docs/reference/engines/table-engines/mergetree-family/versionedcollapsingmergetree).
- Selected the ClickHouse time-series response format for both line charts.
  The events query now returns distinct labeled numeric series instead of a
  table containing the event-name string column.

The Grafana rollout exposed four stale WHOOP volume/mount fields still owned
by `argocd-controller` from September. Helm's new manifest did not contain
them, but server-side field ownership kept them alive after the ConfigMap was
removed. A guarded JSON patch removed only these four obsolete fields to match
Git, and the rollout completed.

Both retained datasources are healthy. All retained panel target queries passed;
empty issue tables and the host with no custom events were checked as expected
empty results rather than connection failures. Existing Prometheus history is
still limited by the earlier persistence incident; query success does not imply
that missing older samples have been recovered. MCP image rendering returned
HTTP 500 because a renderer is unavailable, so this audit verifies queries and
frame schemas, not a pixel-level browser render.

## Follow-up: Flux metrics and upstream dashboards

Added a 30-second PodMonitor for the four installed Flux controllers and a
Prometheus-only TCP 8080 egress allowance. Existing Flux bootstrap ingress
already allows scraping. Extended the existing kube-state-metrics with seven
Flux resource kinds and scoped list/watch RBAC while preserving all standard
Kubernetes collectors. No controller restart or persistent-data migration was
required.

Provisioned **Flux Cluster Stats** (`flux-cluster`) and **Flux Control Plane**
(`flux-control-plane`) in the Grafana Flux folder from the official monitoring
example at `7ab65dc8b90f7a6751d88f18bbb4e1bee33bf334`, preserving its Apache
license. Local adaptations pin the Prometheus UID and namespace defaults and
make healthy failing-resource stats display zero without masking an absent
base metric. The source and adaptation details are in the monitoring README.

Live checks after scrape warm-up and normal reconciliation events:

- Four of four controller targets up; zero down targets across Prometheus.
- `gotk_resource_info` exposed 85 resources, matching Kubernetes exactly:
  28 Kustomizations, 24 HelmReleases, 1 GitRepository, 8 HelmRepositories,
  12 HelmCharts and 12 OCIRepositories; zero Buckets or suspended resources.
- All Kustomizations and HelmReleases Ready; controller operations, durations,
  CPU/memory and resource-readiness frames contained live data.
- All 35 active target queries across the 27 new data panels succeeded. Only
  the Suspended Objects table was empty, matching the Kubernetes state.
- Re-ran the 54 queries across the original 53 panels without query errors;
  both datasources stayed healthy and all nine CNPG collectors remained up.

New Flux metric history starts when this collection was enabled. The existing
MCP image-renderer limitation still applies; verification used real backend
query results and frame schemas.

## Supabase persistence and operator migration (cutover pending)

- Recovered the legacy PostgreSQL database and pgsodium configuration inside the
  cluster, verified file checksums and an isolated restore, and retained the
  original PVCs plus `supabase-db-recovery-20261112`. No full database or key
  export was written to the Mac. This retained copy is on-node, not an off-node
  backup; VM backups remain disabled as requested.
- Corrected the legacy chart's PostgreSQL mount and shutdown command. Added and
  applied the Talos kubelet shared bind mount for local-path storage so the new
  operator's `subPath` mounts resolve to the persistent XFS disk.
- Installed `supabase-operator` and `supabase-project` charts `0.8.4` from master.
  The existing PostgreSQL 17.6.1.136 database and pgsodium key were copied into
  the new project's PVC and verified before startup. Initial bootstrap SQL is
  disabled for the already-initialized database. All ten enabled project CRs
  became Ready.
- Preserved the original database password, JWT secret, anon/service-role keys,
  dashboard login, Realtime/Meta crypto keys and Storage credentials. Existing
  credentials merge through ESO. Seven newly generated operator key fields
  remain only in Kubernetes until personal 1Password CLI access is restored:
  Connect reads the existing item but its write request returned HTTP 403.
- Private checks passed for Auth health, REST table reads with the old anon key
  and new publishable key, Storage status, Studio authentication, Meta health,
  missing-credential rejection and public-only JWKS. A synthetic row survived
  database pod recreation; the database identifier stayed unchanged. Restarting
  the operator preserved all five credential Secrets. The test table and copy
  helper were removed afterward.
- Public cutover and legacy HelmRelease retirement are pending vaulting the new
  keys and wiring their ESO mappings. The existing public hostname still serves
  the legacy installation. See `apps/supabase/README.md` for the remaining steps.
