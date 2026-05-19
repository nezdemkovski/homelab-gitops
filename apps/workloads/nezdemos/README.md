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

## Secrets

The source of truth is 1Password:

```text
Homelab/nezdemos-whoop-scraper
```

The item contains the database password and WHOOP OAuth fields. Token/client
fields can stay empty until the WHOOP app credentials are ready.
