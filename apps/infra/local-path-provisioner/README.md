# Local Path Provisioner

Single-node local persistent storage for the homelab cluster.

The chart is pinned in `application.yaml`. It creates the default `local-path`
StorageClass and stores provisioned volumes under:

```text
/var/lib/local-path-provisioner
```

This is local node storage. PVC data stays on the Talos node and is not
replicated elsewhere.

The namespace is labeled with `pod-security.kubernetes.io/enforce=privileged`
because the provisioner creates helper pods that use `hostPath` volumes.
