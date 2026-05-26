# Fizzy

Fizzy runs from the local Helm chart in:

```text
charts/fizzy
```

The image is pinned by digest in `charts/fizzy/values.yaml`:

```text
ghcr.io/basecamp/fizzy@sha256:8ee159ba1218759de8a8ea0eea823c5869ad8ec8d5abd2f5c7db8891a75e0cbb
```

Data is stored in:

```text
fizzy/fizzy-data
```

Fizzy stores its SQLite database and Active Storage files under
`/rails/storage`.

Secrets are stored in 1Password:

```text
Homelab/fizzy
```

The public hostname is:

```text
fizzy.nezdemkovski.cloud
```

Email is not configured yet. Fizzy can still be tested by reading the
six-character sign-in verification code from the container logs.
