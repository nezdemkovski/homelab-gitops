# Forgejo

Flux deployment for the existing Forgejo installation. The chart and image are
pinned to the versions currently running under Argo CD so ownership can move
without an application upgrade.

## Persistent state

Forgejo stores SQLite, repositories, SSH host keys, attachments, packages,
avatars, indexes, queues, and Actions data on the existing
`gitea-shared-storage` PVC mounted at `/data`. The chart keeps this claim on
Helm uninstall, and the Flux Kustomization orphans resources when deleted.

The cluster Kustomization is intentionally suspended while Argo CD owns the
release. Resume it only during the controlled handoff after taking an offline
backup and stopping Argo reconciliation.

## Handoff checks

Before resuming Flux:

1. Disable automated sync and remove the resource finalizer from the Argo CD
   `forgejo` Application without deleting its managed resources.
2. Scale the Forgejo Deployment to zero and wait for the pod to terminate.
3. From a temporary pod mounting `gitea-shared-storage`, archive all of `/data`
   to storage outside the cluster node. Record the archive SHA-256 and the
   SQLite `PRAGMA integrity_check` result.
4. Record repository count and run `git fsck --full --no-dangling` for every
   bare repository below `/data/git/gitea-repositories`.
5. Delete only the Argo CD Application object, confirm the PVC remains Bound,
   then remove `spec.suspend` here and reconcile the Flux Kustomization.

After Flux reports Ready, verify `/api/healthz`, the public web URL, SSH cloning
on port `30022`, SQLite integrity, repository count, and a sample clone. Keep
the external backup until those checks pass.
