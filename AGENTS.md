# AGENTS.md

Operational rules for agents working in this repository.

## App Control

The root Argo CD application recursively applies manifests under `apps/`.
It ignores these paths:

```text
**/*.disabled
**/_disabled/**
```

Use this convention when enabling or disabling services:

```text
apps/workloads/<app>/application.yaml           enabled
apps/workloads/<app>/application.yaml.disabled  disabled
apps/workloads/<app>/_disabled/                 disabled scratch area
```

For apps installed as child Argo CD `Application` resources, disable the app by
renaming `application.yaml` to `application.yaml.disabled`. The root app prunes
the child application, and the child application's finalizer prunes the
Kubernetes resources it owns.

For raw manifests applied directly by the root app, move the manifest into
`_disabled/` or rename it with `.disabled`.

Before disabling stateful apps, check the PVCs:

```bash
kubectl -n <namespace> get pvc
```

PVC deletion depends on the chart and storage reclaim behavior. Treat app
disable as service removal, not as a backup strategy.

## Version Pins

Always pin chart and image versions in Git:

```yaml
targetRevision: <chart-version>
helm:
  valuesObject:
    image:
      tag: <app-version>
```

Do not rely on chart defaults such as `latest` or `stable`. Updates should be a
normal Git change so Renovate or another bot can open PRs later.

Renovate is configured in `renovate.json`. Keep Argo CD applications under
`apps/infra/**/application.yaml` or `apps/workloads/**/application.yaml` so the
`argocd` manager can detect Helm chart and image pins. Raw Kubernetes manifests
under `apps/infra/**` and `apps/workloads/**` are scanned by the `kubernetes`
manager.

When adding a new service, also add a matching Renovate `packageRules` entry
that groups updates by the deployed app boundary. If the app has both an Argo CD
application and a local chart, include both paths, for example
`apps/workloads/<app>/**` and `charts/<app>/**`. This keeps chart bumps, app
image bumps, and sidecar image bumps in one reviewable PR for that service.

## Secrets

Secrets live in the `Homelab` 1Password vault. External Secrets Operator syncs
them into Kubernetes.

Do not commit generated secrets, Cloudflare Tunnel credentials, kubeconfigs, or
service credentials.

## Network Policies

Cilium enforces Kubernetes `NetworkPolicy` resources in this cluster.

Workload namespaces are deny-by-default through:

```text
apps/infra/network-policies/workload-baseline.yaml
```

When adding a new public service:

1. Add its namespace to `homelab-default-deny`.
2. Add `homelab-workload-egress` for DNS, Kubernetes API, same-namespace pod
   traffic, and public internet egress.
3. Add `homelab-same-namespace-ingress` unless the chart already creates
   tighter app-specific policies.
4. Add `homelab-cloudflared-ingress` if Cloudflare Tunnel should expose it.
5. Add its namespace to `homelab-cloudflared-egress` so cloudflared can reach
   the service.

Do not allow broad cross-namespace traffic by default. Add explicit policies for
real dependencies, for example Grafana to PostgreSQL or OpenMarkers to Auth.

LAN egress is intentionally blocked by the workload baseline because private
ranges are excluded from public internet egress. If a service needs to reach
home-network hosts such as `10.77.77.0/24`, add a narrow, named policy for that
service and document why it exists.

## Public Hostnames

Public hostnames are stable service contracts. Prefer naming them by purpose,
not by the implementation currently serving them.

Cloudflare Tunnel ingress rules and public hostnames are intentionally stored
in Git under:

```text
apps/infra/cloudflared/configmap.yaml
```

The Cloudflare Tunnel credentials file stays outside Git in 1Password at
`Homelab/cloudflare-homelab-k8s/credentials.json`.

When changing the tunnel ingress ConfigMap, also bump
`homelab.nezdemkovski.cloud/config-revision` on the cloudflared Deployment pod
template so Argo rolls the pods and cloudflared reads the new config.
