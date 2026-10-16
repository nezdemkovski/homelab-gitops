# Playdamnit deployment

The canonical public origin is `https://playdamnit.com`. Cloudflared sends `/api/*` to
`playdamnit-api` and other paths to `playdamnit-web`. The web image redirects
`www.playdamnit.com` requests to the canonical origin, preserving paths and query strings.
The previous hostname is retired: its tunnel routes and DNS record have been removed.
Installed iOS versions must use the new origin; IGDB callbacks are registered on it.

Cloudflare DNS is managed with `cf`: the apex has a proxied CNAME to the tunnel ID in
`charts/cloudflared/values.yaml`, and `www` has a proxied CNAME to the apex. These DNS records
are separate from the Git-managed ingress configuration.

Auth callbacks, email links and passkey rpID use `BETTER_AUTH_URL` in the API ExternalSecret.
`TRUSTED_ORIGINS` accepts only the canonical origin. The verified Resend sending domain is
`playdamnit.com`; account emails use `noreply@playdamnit.com`.

The librarian registers IGDB callbacks using `WEBHOOK_BASE_URL`. After changing either
ExternalSecret, verify a fresh ESO refresh and roll the consuming deployment: changing Secret
data alone does not reload environment variables in running pods.

The web build in the product repository must use `VITE_API_URL=https://playdamnit.com`.
The iOS production API URL and associated domains are maintained in `playdamnit-ios`.
Its bundle ID remains stable so installs, Sign in with Apple and AASA app IDs stay compatible.
Browser sessions and existing passkeys belong to the old domain; members must sign in and
register a new passkey on the new origin.
