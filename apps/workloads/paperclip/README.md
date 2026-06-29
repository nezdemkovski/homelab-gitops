# Paperclip

Self-hosted Paperclip AI instance.

The service is exposed at `paperclip.nezdemkovski.cloud` through Cloudflare
Tunnel.

Runtime state is stored in:

```text
paperclip/paperclip-data
paperclip/paperclip-postgres
```

Runtime secrets live in 1Password:

```text
Homelab/paperclip
Homelab/paperclip-postgres
```

The image is pinned by digest in `charts/paperclip/values.yaml`. The adjacent
`image.release` field is tracked by Renovate against upstream GitHub releases so
release PRs appear even though the deployed image itself remains digest-pinned.
