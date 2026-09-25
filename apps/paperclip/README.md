# Paperclip

Flux adopts the existing `paperclip` namespace and its data in place. The
initial HelmRelease deliberately preserves the stopped state: the application
has zero replicas, the CloudNativePG cluster remains hibernated, and scheduled
backups remain suspended.

Persistent state remains on the existing claims:

- `paperclip-data` for Paperclip home and agent state
- `paperclip-postgres-1` for the CloudNativePG database

The namespace and application PVC opt out of Flux pruning. The PostgreSQL
Cluster carries Helm's `keep` resource policy so removing the HelmRelease does
not delete the database cluster. The `local-path` StorageClass also retains the
underlying volumes.

Before enabling Paperclip, resume PostgreSQL while the application stays at
zero replicas, verify the database, and complete a fresh object-store backup.
Only then set `replicaCount` to `1`, `postgres.hibernated` to `false`, and
`postgres.backup.suspend` to `false` in the HelmRelease.
