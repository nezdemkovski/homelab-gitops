# Metrics Server

Metrics Server provides the Kubernetes `metrics.k8s.io` API used by:

```text
kubectl top nodes
kubectl top pods
```

It is installed by Argo CD from the official Kubernetes SIGs Helm chart:

```text
https://kubernetes-sigs.github.io/metrics-server/
```

The chart version is pinned in `application.yaml` as `targetRevision`.

This is not long-term monitoring. It only exposes current CPU and memory usage.
Use Prometheus/Grafana later for history, dashboards, and alerts.

The Talos homelab uses:

```text
--kubelet-preferred-address-types=InternalIP
--kubelet-insecure-tls
```

`--kubelet-insecure-tls` is needed because the local kubelet serving certificate
is not trusted by Metrics Server by default.
