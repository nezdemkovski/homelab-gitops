# Cilium Flux handoff

This directory is intentionally referenced by a suspended cluster
`Kustomization`. Cilium is the cluster CNI, so the ownership handoff must be
staged independently from ordinary application migrations.

The Argo application and this HelmRelease use the same release name, namespace,
chart version, and values. Flux explicitly enables Helm take-ownership because
Argo did not create Helm release storage. Cilium's chart uses live `lookup`
calls to preserve the existing CA and Hubble certificates; drift detection also
ignores Secret data for the three generated TLS Secrets.

Before activation:

1. Confirm Cilium, the operator, Hubble, node readiness, and cluster DNS are
   healthy. Record workload UIDs and pod-template hashes.
2. Disable Argo automated sync and remove the Cilium Application finalizer
   without deleting its managed resources.
3. Run a server-side Helm dry-run with `--take-ownership` against chart 1.20.2.
   Abort if the Cilium or Cilium Envoy DaemonSet pod templates differ.
4. Unsuspend only the `cilium` Flux Kustomization and wait for the HelmRelease
   and all Cilium workloads to become Ready.
5. Confirm the recorded UIDs, node readiness, DNS, API access, Hubble, and
   external application connectivity before removing the Argo Application.

Do not activate `cloudflared` until the Cilium handoff has passed these checks.
