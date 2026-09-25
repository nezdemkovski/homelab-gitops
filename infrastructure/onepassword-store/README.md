# 1Password secret store

External Secrets uses the in-cluster 1Password Connect service through the
cluster-wide `onepassword` store. The bootstrap Secrets named
`op-credentials` and `onepassword-connect-token` are intentionally not stored
in Git and must remain in the `external-secrets` namespace.
