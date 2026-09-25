# Forgejo

Flux reconciles the Forgejo HelmRelease in the `forgejo` namespace.

Forgejo stores SQLite, repositories, SSH host keys, attachments, packages,
avatars, indexes, queues, and Actions data on the `gitea-shared-storage` PVC
mounted at `/data`. The namespace is protected from Flux pruning and the chart
marks the claim with Helm's keep policy.

Before changing storage, the release name, or chart persistence values:

1. Stop writes and take an archive of `/data` outside the cluster node.
2. Record the archive SHA-256 and run SQLite `PRAGMA integrity_check`.
3. Run `git fsck --full --no-dangling` on the bare repositories.
4. Verify the PVC UID and bound PV before and after reconciliation.

After an upgrade, verify `/api/healthz`, the public web URL, SSH cloning on
port `30022`, SQLite integrity, repository count, and a sample clone.
