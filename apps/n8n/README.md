# n8n Flux handoff

This directory prepares Flux to adopt the existing `n8n` namespace in place.
The cluster Kustomization is intentionally committed with `spec.suspend: true`;
it must stay suspended until Argo CD automation and its resource finalizer have
been disabled for the `n8n` Application.

## Persistent state

The active data claims observed before this handoff are:

- `n8n-postgres-cnpg-1`: active CloudNativePG database claim.
- `n8n`: `/home/node/.n8n`, including installed nodes, caches, binary data,
  uploads, SSH state, and local application files.

The chart references `n8n` through `persistence.existingClaim`, so Helm does not
create or delete the application claim. The namespace, application PVC, and
CloudNativePG Cluster opt out of Flux pruning. The cluster Kustomization also
uses `deletionPolicy: Orphan`.

`data-n8n-postgres-0` is a legacy PostgreSQL rollback claim. It is not mounted
by the active n8n or CloudNativePG pods and is deliberately absent from the
Flux manifests. Keep it until the Flux deployment and a restore test have both
been verified, then remove it as a separate cleanup operation.

The encryption key remains sourced from the existing `n8n` 1Password item via
the `n8n-env` ExternalSecret. It is required to decrypt all saved credentials.

## Pre-handoff baseline (2026-09-25)

- Public health: `https://automations.nezdemkovski.cloud/healthz` returned 200.
- PostgreSQL: `n8n-postgres-cnpg` healthy, primary
  `n8n-postgres-cnpg-1`, latest scheduled object-store backup completed.
- Database size: 69,228,211 bytes.
- Key rows: 10 workflows, 7 credentials, 2 executions, 1 user, 1 project.
- Appdata: about 468 MiB; `binaryData` existed and contained zero files at the
  time of inspection.

Counts are a comparison baseline, not desired state. Repeat them after stopping
writes and again after Flux starts n8n.

## Safe handoff

1. Confirm ExternalSecrets are Ready and record fresh PostgreSQL row counts and
   appdata size.
2. Create a uniquely named CloudNativePG `Backup` and wait for phase
   `completed`. Keep the existing scheduled backup enabled.
3. Disable Argo CD automated sync and remove only the n8n Application's resource
   finalizer. Scale `n8n-main` to zero so workflows cannot write during the
   ownership transition. Leave CloudNativePG running.
4. Change only `clusters/homelab/n8n.yaml` to `spec.suspend: false`, push it to
   the Flux branch, and reconcile the source and Kustomization with the Flux
   CLI. The HelmRelease uses Helm take-ownership and the same release, workload,
   Service, PVC, database host, chart, and image versions.
5. Wait for the OCIRepository, HelmRelease, Kustomization, Deployment,
   ExternalSecrets, and CloudNativePG Cluster to be Ready. Verify the same PVC
   UIDs remain bound.
6. Compare database counts, confirm saved credentials decrypt by running an
   existing workflow, inspect `/home/node/.n8n`, and check the public health URL.
7. Delete the Argo Application and its manifests only after Flux verification.
   Keep the legacy PostgreSQL PVC until a separate restore test succeeds.
