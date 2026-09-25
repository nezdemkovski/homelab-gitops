# Cilium

Flux manages Cilium as release `cilium` in `kube-system`. Cilium is the
cluster CNI, so upgrades require a separate maintenance check from ordinary
application changes.

The chart uses live `lookup` calls to retain the existing CA and Hubble
certificates. Drift detection ignores data in the generated Cilium TLS Secrets.

Before an upgrade, record Cilium, operator, Hubble, node, DNS, API, and public
endpoint health. Render the candidate Helm release and review DaemonSet and
operator pod-template changes. Reconcile only the `cilium` Kustomization, wait
for its HelmRelease and workloads, then repeat the same connectivity checks.
