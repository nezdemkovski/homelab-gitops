# Argo CD Project

`project.yaml` is the live GitOps-managed `homelab` AppProject. The root app
syncs this directory, so destination/source allowlist changes are applied from
Git instead of by hand.

`bootstrap/project.yaml` is kept as the first-install seed. Keep it identical
to this file when changing project policy.
