# Homelab GitOps

Declarative Kubernetes configuration for the Talos homelab cluster.

Argo CD watches this repository and reconciles manifests from `apps/`.

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
