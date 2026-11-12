# Local path storage on Talos

`local-path` uses `/var/lib/local-path-provisioner`, with `Retain` reclaim policy.
The Talos kubelet must bind this path from the host; otherwise PVC `subPath`
mounts can resolve into kubelet's disposable container overlay.

The non-secret `talos-kubelet-mount.patch.yaml` records the required machine
configuration. This is a Talos patch, deliberately not a Kubernetes resource in
this directory's Kustomization. Preserve any other kubelet extra mounts when
merging it into the machine configuration.

Apply with global Talos context `homelab`, first using `--dry-run`, then
`--mode no-reboot`. A kubelet restart can occur; verify node readiness, the
kubelet's host bind mount, actual workload mount filesystems and data after a
pod recreation. Flux continues to reconcile Kubernetes resources separately.
