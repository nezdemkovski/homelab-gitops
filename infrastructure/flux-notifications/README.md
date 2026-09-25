# Flux Telegram notifications

The `flux-notifications` Kustomization depends on `onepassword-store`.
External Secrets copies `Homelab/homelab-fluxcd/TELEGRAM_BOT_TOKEN` into the
`flux-system/flux-telegram-token` Secret as `token`. The Flux Telegram Provider
sends to the owner's private chat.

`telegram-errors` forwards only error events from the Git source, all
Kustomizations and image automation in `flux-system`, plus HelmReleases in the
listed namespaces. When adding a HelmRelease in a new namespace, add that
namespace to `alert.yaml`.

These are GitOps reconciliation errors, not general pod or host-health alerts.
Use Prometheus/Alertmanager for runtime availability and node alerts.
