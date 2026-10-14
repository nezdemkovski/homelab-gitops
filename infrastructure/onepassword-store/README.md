# 1Password secret store

External Secrets uses the in-cluster 1Password Connect service through the
cluster-wide `onepassword` store. The bootstrap Secrets named
`op-credentials` and `onepassword-connect-token` are intentionally not stored
in Git and must remain in the `external-secrets` namespace.

## Vault layout

The `Homelab` vault has one active Secure Note per service, without tags.
Keep application keys, database credentials and registry credentials in sections
of that item rather than separate `*-postgres`, `*-redis` or `*-ghcr` items. Shared services retain
their own item: for example, `synology-rustfs` owns backup storage credentials;
consumers reference that item instead of copying the credentials.

Use unique field labels within an item; External Secrets selects those labels.
Application-specific API keys keep their existing descriptive names. Database
and registry fields use these labels:

| Section | Fields |
| --- | --- |
| PostgreSQL | `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_URL` |
| PostgreSQL access from a Mac | `DB_PORT_FORWARD`, `DB_LOCAL_URL` |
| PostgreSQL read-only account | `DB_READER_USER`, `DB_READER_PASSWORD`, `DB_READER_URL` |
| Redis | `REDIS_HOST`, `REDIS_PORT`, `REDIS_PASSWORD`, `REDIS_URL` |
| ClickHouse | `CLICKHOUSE_HOST`, `CLICKHOUSE_PORT`, `CLICKHOUSE_DATABASE`, `CLICKHOUSE_USER`, `CLICKHOUSE_PASSWORD`, `CLICKHOUSE_URL` |
| Container registry | `GHCR_USER`, `GHCR_TOKEN` |

Passwords, tokens and connection strings containing credentials are concealed
fields. URL-encode credentials in connection strings. `DB_URL` uses Kubernetes
service DNS and is reachable from the cluster. From a Mac, run the item's
`DB_PORT_FORWARD` command, then connect with `DB_LOCAL_URL` while the forwarding
session is open. Commands use `kubectl --context admin@homelab` and the global
`~/.kube/config`, without repository paths. PostgreSQL forwarding uses local port
`15432`; stop the previous session before forwarding another service.

`amela` includes backend, frontend, PostgreSQL and registry fields. `auth`
includes PostgreSQL and Redis. `nezdemos` includes API, WHOOP and database reader
credentials. `grafana` owns the MCP token; database reader credentials belong to
the database's service. `cloudflared` owns tunnel credentials and `flux` owns
notification credentials. `onepassword` owns the ESO service-account credentials.
Recovery attachments remain in the separate `kubernetes` and `talos` items.

FNPC, Nezdemos and NocoDB are not deployed in the current cluster. Their saved
connection details are historical, marked by `DB_STATUS`, and must be verified
before reuse. Old charts outside this repository may still default to retired
item names; supply the canonical item and field labels before redeploying them.

When reorganizing items, populate the destination first, update references in
Git, reconcile Flux and force-refresh the affected ExternalSecrets. Verify Ready
conditions and unchanged consumer Secret data before archiving source items.
Keep archived items recoverable; do not permanently delete them as part of cleanup.

## Local client configuration

See [global config paths and contexts](../../README.md#access). Recovery
attachments and client commands are recorded in the `kubernetes` and `talos`
Secure Notes. Preserve other contexts when restoring; never put configs in Git.
