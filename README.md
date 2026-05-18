# Homelab GitOps

Declarative Kubernetes configuration for the Talos homelab cluster.

## Bootstrap

Install Argo CD once, then apply the root application:

```bash
export KUBECONFIG=/Users/yuri/Sites/homelab-gitops/kubeconfig

kubectl create namespace argocd
kubectl apply -n argocd --server-side --force-conflicts \
  -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

kubectl apply -f bootstrap/project.yaml
kubectl apply -f bootstrap/root-app.yaml
```

After that, add or update manifests under `apps/` and let Argo CD reconcile them.

## Layout

```text
bootstrap/      Argo CD resources applied manually once.
apps/infra/     Cluster infrastructure apps like ingress, cert-manager, storage.
apps/workloads/ User applications.
```

## App Control

The root Argo CD application recursively applies manifests under `apps/`.
It ignores:

```text
**/*.disabled
**/_disabled/**
```

Use this convention to keep services easy to control from Git:

```text
apps/workloads/<app>/application.yaml           enabled
apps/workloads/<app>/application.yaml.disabled  disabled
apps/workloads/<app>/_disabled/                 disabled scratch area
```

For apps installed as child Argo CD `Application` resources, disabling means
renaming `application.yaml` to `application.yaml.disabled`. The root app prunes
the child application, and the child application's finalizer prunes the
Kubernetes resources it owns.

For raw manifests that are applied directly by the root app, move the manifest
into `_disabled/` or rename it with `.disabled`.

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

## Secrets

Secrets and public hostnames live in the `Homelab` 1Password vault. External
Secrets Operator syncs them into Kubernetes. Do not commit generated secrets,
Cloudflare Tunnel credentials, kubeconfigs, or public service hostnames.
