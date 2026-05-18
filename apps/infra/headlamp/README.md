# Headlamp

Headlamp is installed by Argo CD from `application.yaml`.

The Helm chart version is pinned in `targetRevision`. Bump that field in a PR
instead of tracking the chart's latest version implicitly.

## Access

Open the UI with a local port-forward:

```bash
export KUBECONFIG=/Users/yuri/Sites/noona/app-storyous/kubeconfig

kubectl -n headlamp port-forward svc/headlamp 8081:80
```

Then open:

```text
http://localhost:8081
```

## Login Token

Headlamp uses a Kubernetes bearer token for login. The current chart creates the
`headlamp/headlamp` service account and binds it to `cluster-admin`, so treat
tokens for it as full cluster admin credentials.

Short-lived token:

```bash
kubectl -n headlamp create token headlamp --duration=24h
```

More convenient homelab token:

```bash
kubectl -n headlamp create token headlamp --duration=720h
```

`720h` is roughly 30 days. Kubernetes may cap the maximum accepted token
duration depending on API server settings.
