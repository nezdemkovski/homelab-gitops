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

## Secrets

Secrets and public hostnames live in the `Homelab` 1Password vault. External
Secrets Operator syncs them into Kubernetes.

Do not commit generated secrets, Cloudflare Tunnel credentials, kubeconfigs, or
public service hostnames.

## Public Hostnames

Public hostnames are stable service contracts. Prefer naming them by purpose,
not by the implementation currently serving them.

Cloudflare Tunnel ingress rules and public hostnames are intentionally stored
outside Git in 1Password at:

```text
Homelab/cloudflare-homelab-k8s/config.yaml
```
