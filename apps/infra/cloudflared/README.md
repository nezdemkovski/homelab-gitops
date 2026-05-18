# cloudflared

This deploys a locally managed Cloudflare Tunnel connector inside the cluster.

```text
Tunnel:   homelab-k8s
ID:       fb9144ee-d450-448f-94ab-530094b85247
Hostname: n8n-homelab.nezdemkovski.cloud
Origin:   http://n8n-main.n8n.svc.cluster.local:5678
```

The tunnel credentials JSON is stored in 1Password:

```text
Homelab/cloudflare-homelab-k8s/credentials.json
```

External Secrets Operator syncs that field into:

```text
cloudflared/cloudflare-tunnel-credentials
```

The main `n8n.nezdemkovski.cloud` hostname currently points at the older `zeus`
tunnel. Switch it later only after verifying the Kubernetes-backed hostname.

