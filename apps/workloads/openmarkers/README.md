# OpenMarkers

OpenMarkers is deployed as a small stack:

- `openmarkers-postgres` - CloudNativePG Postgres cluster
- `openmarkers` - application chart from `oci://ghcr.io/nezdemkovski/charts`

Secrets are stored in 1Password:

```text
Homelab/openmarkers-postgres
Homelab/openmarkers
```

The public hostname is routed through the shared Cloudflare Tunnel.

## MCP

The remote MCP endpoint is:

```text
https://openmarkers.app/mcp
```

OpenMarkers is the OAuth protected resource server. It delegates auth to:

```text
https://auth.nezdemkovski.cloud/openmarkers
```

The workload accepts both browser session JWTs and OAuth access JWTs through
`AUTH_JWT_AUDIENCE`. Keep `https://openmarkers.app/mcp` in that audience list
when changing auth or domain settings, otherwise remote MCP token exchange will
succeed but OpenMarkers will reject the token.
