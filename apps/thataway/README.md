# Thataway deployment

The places API behind the Thataway iOS app, public at `https://thataway.nezdemkovski.cloud`
through the Cloudflare tunnel (`charts/cloudflared/values.yaml`); the DNS record is a proxied
CNAME to the tunnel, managed with `cf`.

The database is a CloudNativePG cluster on the PostGIS image. Its owner credentials live in the
`thataway` Secure Note in the Homelab vault (`DB_USER`, `DB_PASSWORD`, with `DB_URL` and the
port-forward command for a Mac); ExternalSecrets turn them into the owner secret the cluster
bootstraps with and into the API's `POSTGRES_URL`. The pull token is the shared GHCR one and the
backup credentials come from `synology-rustfs`. The API's init container applies the migrations.

Egress to the internet is required: the API fills its database from Wikidata, Wikipedia and
Wikimedia Commons (`infrastructure/network-policies/workload-thataway.yaml`).
