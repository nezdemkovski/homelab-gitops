# Auth

Central Better Auth service for project-scoped user pools.

The service is exposed at `auth.nezdemkovski.cloud` through Cloudflare Tunnel.
Runtime secrets live in 1Password:

- `Homelab/auth`
- `Homelab/auth-postgres`

`AUTH_PROJECTS` currently lives in `Homelab/auth` and starts as an empty JSON
array. Add projects there after the application has project schema lifecycle and
migrations.

## Email

Cloudflare Email Service support is wired but disabled by default.

To enable outbound verification and password reset emails:

- onboard the sending domain in Cloudflare Email Sending;
- add `CLOUDFLARE_EMAIL_API_TOKEN` to `Homelab/auth`;
- set `env.email.provider: cloudflare`;
- set `env.email.cloudflareAccountId` to the Cloudflare account ID;
- keep `env.email.from` on an onboarded sender domain.
