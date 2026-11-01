# Doop

Public URL: https://doop.nezdemkovski.cloud. One process serves the web client,
API, WebSocket rooms and OAuth MCP endpoint (`/mcp`) on port 4400. Keep one replica
and Recreate updates: rooms and upload tickets live in memory.

## Release

Unmodified upstream v0.12.0, source commit
`65b24a5ee0696f2646720cf57727e68873cd6fba` (AGPL-3.0).
The manual `Build Doop` workflow builds the upstream Dockerfile, including
Chromium, and publishes `ghcr.io/nezdemkovski/doop`. The deployment pins the image
by version and digest. To update, review upstream changes/migrations, change the
source SHA and version in the workflow, run it, and pin its output digest here.
Do not roll back across incompatible database migrations without restoring a
compatible backup. Startup applies upstream Drizzle migrations automatically.

## Data and secrets

CloudNativePG owns `doop-postgres`, with a 5 GiB Retain local-path volume. The
namespace and database have prune disabled. Daily backups run at 03:30 UTC,
with continuous WAL archiving and 30-day retention, in
`s3://cnpg-backups/doop-postgres` on the NAS. The first backup runs immediately.

Uploads and thumbnails use the private, versioned `doop-assets` RustFS bucket
at `http://10.77.77.190:9000`. The application proxies asset reads; the bucket
needs no public policy or separate tunnel route. Versioning preserves overwritten
or deleted objects, but the bucket still shares the NAS failure domain.

Runtime credentials are ExternalSecrets backed by the Homelab vault:

- `doop`: database credentials, signing secret, admin email, registration domain.
- `synology-rustfs`: shared S3 credentials for assets and backups.
- `auth`: existing Resend SMTP key and verified sender.
- `amela`: existing shared read-only GHCR credential; publication uses the
  workflow's temporary GITHUB_TOKEN, with no persistent write token.

Registration is limited to `nezdemkovski.com`, with mandatory email verification.
The verified configured admin gains the admin role. Create the account through
the UI; no preset login password exists. SMTP enables verification and resets.
No server-paid AI allowance or model key is configured. Connect an external MCP
agent or configure a model account in Doop to run real design tasks.

Network policies allow DNS, same-namespace traffic, CNPG operator management,
Kubernetes API access for database pods, NAS S3, public HTTP/HTTPS and Resend SMTP.
Only the tunnel may enter the app from another workload namespace.
