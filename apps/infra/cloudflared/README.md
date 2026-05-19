# cloudflared

This deploys a locally managed Cloudflare Tunnel connector inside the cluster.

The tunnel ID, public hostnames, and ingress rules are managed in Git through
the local chart:

```text
charts/cloudflared
```

The tunnel credentials JSON stays in 1Password:

```text
Homelab/cloudflare-homelab-k8s/credentials.json
```

External Secrets Operator syncs that field into:

```text
cloudflared/cloudflare-tunnel-credentials
```
