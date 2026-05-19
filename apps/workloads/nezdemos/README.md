# NezdemOS

NezdemOS is the personal services stack. Small scrapers, importers, bots, APIs,
and dashboards can live here when they share personal data.

## PostgreSQL

PostgreSQL is managed by CloudNativePG:

```text
cluster:  nezdemos-postgres
database: nezdemos
service:  nezdemos-postgres-rw.nezdemos.svc.cluster.local:5432
```

Use one schema per source or service. The first schema is:

```text
whoop
```

For Grafana, prefer connecting read-only later and querying explicit schemas
such as `whoop.whoop_sleep` and `whoop.whoop_recovery`.

Database ownership is stack-level:

```text
owner role: nezdemos
app role:   whoop_scraper
```

App roles should only receive the privileges they need for their own schema.
Do not use app roles as database owners.

## Secrets

The source of truth is 1Password:

```text
Homelab/nezdemos-postgres       database owner credentials
Homelab/nezdemos-whoop-scraper
```

The `nezdemos-whoop-scraper` item contains the app database password, WHOOP
client credentials, and the token encryption key. Access and refresh tokens are
not stored in 1Password; the `whoop-scraper auth` flow writes them into
`whoop.whoop_oauth_tokens`.
