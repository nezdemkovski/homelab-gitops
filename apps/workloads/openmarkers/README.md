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
