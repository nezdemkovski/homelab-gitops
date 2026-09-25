# Flux Telegram notifications

The `flux-notifications` Kustomization depends on `onepassword-store`.
External Secrets copies `Homelab/homelab-fluxcd/TELEGRAM_BOT_TOKEN` into the
`flux-system/flux-telegram-token` Secret as `token`. The Flux Telegram Provider
sends to the owner's private chat.

`telegram-errors` forwards only error events from the Git source, all
Kustomizations and image automation in `flux-system`, plus HelmReleases in the
listed namespaces. When adding a HelmRelease in a new namespace, add that
namespace to `alert.yaml`.

`telegram-image-updates` reports only commits pushed by Flux image automation.
The commit means Git has new image pins; workloads may still be reconciling.
`telegram-chart-upgrades` reports successful upgrades of externally sourced
Helm charts. Local GitRepository charts are excluded because their revision
changes after unrelated Git commits. Add new external HelmReleases to its
event sources.

`telegram-available-images` reports changes selected by the unbounded
`*-latest` ImagePolicies. These policies are discovery only: an upstream
version may be available even though the bounded deployment policy has not
adopted it. Review compatibility and backups before widening a stateful or
infrastructure range. New image discovery policies must be added to this
alert's event sources.

These alerts cover GitOps reconciliation and version changes, not general pod
or host health. Use Prometheus/Alertmanager for runtime availability and node
alerts.
