# Auth

Central Better Auth service for project-scoped user pools.

The service is exposed at `auth.nezdemkovski.cloud` through Cloudflare Tunnel.
The workload uses the published OCI Helm chart:

```text
oci://ghcr.io/nezdemkovski/charts/auth
```

Runtime secrets live in 1Password:

- `Homelab/auth`
- `Homelab/auth-postgres`
- `Homelab/auth-redis`

The chart deploys the auth stack as separate components:

- `auth-api` - Bun/Hono Better Auth API.
- `auth-admin` - static admin dashboard.
- `auth-login` - static user-facing login experience.
- `auth-router` - internal Caddy router behind the stable `auth` Service.

Application realms are managed from the admin dashboard. The service keeps realm
metadata in Postgres and creates the per-realm schema and Better Auth tables
automatically when a new realm is added.

## Email

Outbound email support is wired but disabled by default.

To enable outbound verification and password reset emails with Resend:

- verify the sender domain in Resend;
- add `RESEND_API_KEY` to `Homelab/auth`;
- keep `EMAIL_FROM` in `Homelab/auth` on a verified sender domain;
- set `env.email.provider: resend`.

Cloudflare Email Service is also supported:

- onboard the sending domain in Cloudflare Email Sending;
- add `CLOUDFLARE_EMAIL_API_TOKEN` to `Homelab/auth`;
- set `env.email.provider: cloudflare`;
- keep `CLOUDFLARE_ACCOUNT_ID` and `EMAIL_FROM` in `Homelab/auth`.
