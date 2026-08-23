# Haymaker

Haymaker runs as one public web deployment, one singleton API deployment, and
one CloudNativePG cluster. The shared Cloudflare Tunnel exposes the site at
`https://haymaker.lol` and the browser API at `https://api.haymaker.lol`.

Runtime credentials are synced from the `haymaker`, `haymaker-postgres`, and
`haymaker-ghcr` items in the Homelab 1Password vault. The initial deployment
uses Polar sandbox credentials and logs email notifications because no Resend
key is configured yet.
