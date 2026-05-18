# External Secrets Operator

External Secrets Operator syncs secrets from external backends into Kubernetes
Secrets.

The chart is pinned in `application.yaml`. CRDs are installed by the chart using
server-side apply because some CRD definitions are too large for normal
client-side apply annotations.

## 1Password Bootstrap

1Password access uses a service account token stored as a Kubernetes Secret:

```text
external-secrets/onepassword-token
```

Create it manually after creating a 1Password service account with `read_items`
access to the `Homelab` vault:

```bash
export KUBECONFIG=/Users/yuri/Sites/homelab-gitops/kubeconfig

kubectl -n external-secrets create secret generic onepassword-token \
  --from-literal=token='ops_...'
```

This bootstrap token is not committed to git.
