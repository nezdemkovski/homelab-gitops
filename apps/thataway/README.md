# Thataway deployment

The places API behind the Thataway iOS app, public at `https://thataway.nezdemkovski.cloud`
through the Cloudflare tunnel (`charts/cloudflared/values.yaml`); the DNS record is a proxied
CNAME to the tunnel, managed with `cf`.

The database is a CloudNativePG cluster on the PostGIS image. The operator generates the
application owner's secret (`thataway-postgres-app`); the API's `POSTGRES_URL` comes from its
`uri` key, so no 1Password item is needed beyond the shared GHCR pull token and the backup
credentials. The API's init container applies the migrations.

Egress to the internet is required: the API fills its database from Wikidata, Wikipedia and
Wikimedia Commons (`infrastructure/network-policies/workload-thataway.yaml`).
