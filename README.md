# Homelab GitOps

Declarative configuration for the Talos Kubernetes homelab. Flux reconciles
`master` from `clusters/homelab`; application releases and infrastructure changes
are deployed through Git.

## Repository layout

| Path | Purpose |
| --- | --- |
| `clusters/homelab/flux-system/` | Flux controllers and Git source/bootstrap configuration |
| `clusters/homelab/*.yaml` | Component Kustomizations and their dependencies |
| `apps/<app>/` | Application manifests and HelmReleases |
| `infrastructure/<component>/` | Controllers, policies and shared cluster services |
| `charts/` | Local Helm charts |
| `.github/workflows/`, `scripts/` | Dependency automation and its trusted review gate |

## Access

Use global client configs with file permissions `0600`:

- Kubernetes: `~/.kube/config`, context `admin@homelab`.
- Talos: `~/.talos/config`, context `homelab`.

```bash
kubectl --context admin@homelab get nodes
flux --context admin@homelab get kustomizations -A
flux --context admin@homelab get helmreleases -A
talosctl --context homelab version
```

Recovery attachments are in the `kubernetes` and `talos` Secure Notes in the
Homelab 1Password vault. Merge restored contexts with existing global configs;
do not keep credential files in this repository.

## Making changes

Follow [AGENTS.md](AGENTS.md) for rendering, reconciliation, data retention and
network rules. Change the owning app/infrastructure path, render it, commit and
push to `master`, then verify Flux readiness and application behavior. Bootstrap
resources are already committed; routine deployment uses reconciliation.

[Renovate](.renovaterc.json5) proposes grouped dependency updates. The
[Dependency Review workflow](.github/workflows/claude-renovate-review.yaml)
reviews them and a trusted gate merges eligible approved revisions. Major updates
and workflow changes remain for human merge; a green review check alone does not
mean an update was approved or deployed.

Runtime secrets come from 1Password Connect through External Secrets Operator.
See [vault conventions and recovery](infrastructure/onepassword-store/README.md).
Public hostnames and tunnel routes are configured in
[`charts/cloudflared/values.yaml`](charts/cloudflared/values.yaml).
