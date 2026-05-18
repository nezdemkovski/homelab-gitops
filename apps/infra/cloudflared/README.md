# cloudflared

This deploys a locally managed Cloudflare Tunnel connector inside the cluster.

The tunnel ID, public hostnames, and ingress rules are stored in 1Password, not
in Git.

The tunnel credentials JSON is stored in 1Password:

```text
Homelab/cloudflare-homelab-k8s/credentials.json
Homelab/cloudflare-homelab-k8s/config.yaml
```

External Secrets Operator syncs that field into:

```text
cloudflared/cloudflare-tunnel-credentials
```

The `config.yaml` key contains the locally managed tunnel ingress rules.
