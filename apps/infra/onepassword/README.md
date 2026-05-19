# 1Password

This config exposes the `Homelab` 1Password vault to External Secrets Operator
through a `ClusterSecretStore` named `onepassword`.

External Secrets talks to a local 1Password Connect server in the
`external-secrets` namespace. Bootstrap credentials are stored only in
Kubernetes:

```text
external-secrets/op-credentials
external-secrets/onepassword-connect-token
```

Do not commit the credentials file or token. The Connect server and token are
scoped to the `Homelab` vault.

1Password Connect references use this format:

```text
remoteRef.key: <item>
remoteRef.property: <field-or-file>
```

For example, the n8n encryption key is referenced as:

```yaml
remoteRef:
  key: n8n
  property: N8N_ENCRYPTION_KEY
```
