# Haymaker

Haymaker runs a Go API, a Vite frontend, and a CloudNativePG cluster. The
shared Cloudflare Tunnel exposes the site at `https://haymaker.lol` and the
API at `https://api.haymaker.lol`. The frontend proxies `/v1`, `/health`, and
`/openapi.*` to the in-cluster API so the browser stays on one origin.

Runtime credentials are synced from the `haymaker`, `haymaker-postgres`, and
`haymaker-ghcr` items in the Homelab 1Password vault. Public traffic stats come
from the self-hosted Plausible instance.
