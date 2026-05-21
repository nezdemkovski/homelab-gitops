# Auth

Central Better Auth service for project-scoped user pools.

The service is exposed at `auth.nezdemkovski.cloud` through Cloudflare Tunnel.
Runtime secrets live in 1Password:

- `Homelab/auth`
- `Homelab/auth-postgres`

`AUTH_PROJECTS` currently lives in `Homelab/auth` and starts as an empty JSON
array. Add projects there after the application has project schema lifecycle and
migrations.
