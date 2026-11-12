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
