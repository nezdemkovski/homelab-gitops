# Paperclip

Flux runs Paperclip in the existing `paperclip` namespace with its original
data. The HelmRelease runs one application replica and a CloudNativePG instance.
Scheduled object-store backups are enabled.

Persistent state remains on the existing claims:

- `paperclip-data` for Paperclip home and agent state
- `paperclip-postgres-1` for the CloudNativePG database

The namespace and application PVC opt out of Flux pruning. The PostgreSQL
Cluster carries Helm's `keep` resource policy so removing the HelmRelease does
not delete the database cluster. The `local-path` StorageClass also retains the
underlying volumes.

The database was resumed before the application and a fresh object-store backup
completed on 2026-09-25. Its public endpoint is
`https://paperclip.nezdemkovski.cloud`.
