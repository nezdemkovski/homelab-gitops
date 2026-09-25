# n8n

Flux reconciles n8n and its CloudNativePG database in the `n8n` namespace.

Persistent state:

- `n8n-postgres-cnpg-1` is the active database claim.
- `n8n` stores `/home/node/.n8n`, installed nodes, caches, uploads, SSH state,
  and local application files.
- `data-n8n-postgres-0` is a detached legacy rollback claim and is not part of
  the Flux manifests.

The namespace, application PVC, and CloudNativePG Cluster opt out of Flux
pruning. The encryption key comes from the `n8n` 1Password item through the
`n8n-env` ExternalSecret and is required to decrypt saved credentials.

Before database or storage changes, create a uniquely named CloudNativePG
Backup, wait for `completed`, and record database counts and appdata size.
After reconciliation, verify PVC UIDs, database counts, saved credential
decryption through an existing workflow, `/home/node/.n8n`, and
`https://automations.nezdemkovski.cloud/healthz`.
