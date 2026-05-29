# Paperclip

Self-hosted Paperclip AI instance.

The service is exposed at `paperclip.nezdemkovski.cloud` through Cloudflare
Tunnel.

Runtime state is stored in:

```text
paperclip/paperclip-data
```

Runtime secrets live in 1Password:

```text
Homelab/paperclip
```

The image is pinned by digest in `charts/paperclip/values.yaml`.
