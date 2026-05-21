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
