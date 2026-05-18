# 1Password

This config exposes the `Homelab` 1Password vault to External Secrets Operator
through a `ClusterSecretStore` named `onepassword`.

The bootstrap service account token is stored only in Kubernetes:

```text
external-secrets/onepassword-token
```

Do not commit the token. The current service account has `read_items` access to
the `Homelab` vault.

1Password SDK references use this format:

```text
<item>/<field>
```

For example, the n8n encryption key is referenced as:

```text
n8n/N8N_ENCRYPTION_KEY
```

