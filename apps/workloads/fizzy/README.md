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

Email is sent through Resend SMTP:

```text
MAILER_FROM_ADDRESS=fizzy@nezdemkovski.cloud
SMTP_ADDRESS=smtp.resend.com
SMTP_PORT=587
SMTP_USERNAME=resend
```

The public hostname is:

```text
fizzy.nezdemkovski.cloud
```

If SMTP delivery breaks, Fizzy still logs the six-character sign-in verification
code in the container logs.
