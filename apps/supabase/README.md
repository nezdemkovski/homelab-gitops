# Supabase

Flux installs the `supabase` community Helm chart from its official chart
repository. The HelmRelease follows the compatible `0.8.x` chart series and
uses the component image versions shipped with that chart.

This is a fresh installation. The chart provisions new `local-path` claims for
PostgreSQL, Storage, Edge Functions, Studio snippets, Deno cache, and pgsodium.
The six `Released` PVs from the previous installation are not rebound. They
remain retained in the cluster until their old data can be discarded explicitly.

Credentials are read from the `supabase` item in the Homelab 1Password vault
through External Secrets. Cloudflare Tunnel exposes Kong and Studio at
`https://supabase.nezdemkovski.cloud`. PostgreSQL stays private to the cluster.

Analytics, Vector, imgproxy, and MinIO are disabled. Email signup uses automatic
confirmation; outbound SMTP is still unconfigured because the existing
configuration points to localhost.
