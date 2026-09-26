# AGENTS.md

Operational rules for agents working in this Flux GitOps repository.

## Reconciliation model

- `master` is the source of truth for the single `homelab` cluster.
- Flux bootstraps from `clusters/homelab/flux-system` and reconciles the
  component Kustomizations declared in `clusters/homelab/`.
- Application manifests live in `apps/<app>/`; shared controllers and cluster
  services live in `infrastructure/<component>/`.
- Keep one Flux Kustomization per application or independently operated
  component. Express ordering with `spec.dependsOn`.
- Generate Flux resources with the Flux CLI when possible, then commit the
  exported YAML. Do not apply long-lived resources by hand.

Before pushing a change, render the whole cluster offline with
[flate](https://github.com/home-operations/flate), as the `Flate` workflow does:

```bash
flate test all --path ./clusters/homelab
```

For a single Kustomization you can also render the affected path:

```bash
flux build kustomization <name> --path ./clusters/homelab --kustomization-file ./clusters/homelab/<name>.yaml
```

After pushing, reconcile through Flux and wait for Ready:

```bash
flux reconcile source git flux-system
flux reconcile kustomization <name> --with-source
flux get kustomizations
```

Use `flux suspend kustomization <name>` only for a bounded maintenance window.
Resume it as soon as the maintenance operation is complete and record any live
change back in Git.

## Data retention

Flux pruning is enabled for workloads so deleting a manifest removes the
corresponding stateless resources. Stateful boundaries must opt out explicitly:

- add `kustomize.toolkit.fluxcd.io/prune: disabled` to namespaces that contain
  persistent application data;
- add the same annotation to Git-managed PVCs and CloudNativePG `Cluster`
  resources;
- keep storage reclaim policies set to `Retain`;
- keep verified backups outside the Kubernetes node.

Before removing or renaming a stateful resource, inspect its PVC/PV binding and
verify a recent restorable backup. Never use namespace deletion as an
application reset or backup mechanism.

## Versions and updates

Pin exact versions in Git: chart `version`, OCIRepository `ref.tag`, and image
`tag` (own images as `tag: x.y.z@sha256:...`). Do not use semver ranges; Flux
deploys exactly what Git says.

Renovate (`.renovaterc.json5`, `.github/workflows/renovate.yaml`) proposes
every new release, including majors. It follows
`onedr0p/home-ops` and the `home-operations/renovate-presets`:

- own images and charts under `ghcr.io/nezdemkovski` and `ghcr.io/amela-io`
  merge automatically on every release;
- upstream patch, digest and minor updates merge automatically 3 days after
  release, once the `Flate` check passes; 0.x minors are treated as breaking
  and open a PR;
- upstream majors open a PR immediately for manual review and merge;
  `claude-renovate-review.yaml` reviews the PR;
- updates are grouped per stack (`apps/<app>` plus its chart or
  `infrastructure/<component>`); each CloudNativePG image update stays with
  its app, and own releases form a separate `<app> release` group.

A PR from Renovate therefore means either an upstream major or an update whose
`Flate` check failed.

Renovate runs self-hosted from GitHub Actions every hour as the
`nezdemkovski-renovate` GitHub App. Its workflow credentials are GitHub
repository secrets (`RENOVATE_APP_CLIENT_ID`, `RENOVATE_APP_PRIVATE_KEY`,
`GHCR_TOKEN`, `CLAUDE_CODE_OAUTH_TOKEN`); they are CI-only and are not
mirrored in 1Password.

Before merging a major of a stateful or infrastructure component, check the
release notes against this repository and verify a recent restorable backup.
Images and charts must keep a `repository`/`registry` next to `tag` in values
so Renovate can detect them. The Renovate Dependency Dashboard issue lists
pending and rate-limited updates.

## Secrets

Secrets live in the `Homelab` 1Password vault. External Secrets Operator reads
them through the cluster-wide `onepassword` ClusterSecretStore. Commit only
ExternalSecret references. Never commit generated Secrets, 1Password Connect
credentials, Cloudflare Tunnel credentials, kubeconfigs, or service tokens.

## Network policies

Cilium enforces Kubernetes and Cilium network policies. Workload namespaces
are deny-by-default. Add the narrowest required ingress and egress rule for a
new dependency, including DNS, Kubernetes API, Cloudflare Tunnel, monitoring,
database, or backup traffic as needed.

Public internet egress excludes private address ranges. Add a documented,
service-specific rule for access to LAN services such as `10.77.77.0/24`.
Validate DNS, API access, public endpoints, database connectivity, and backup
traffic after changing shared policies.

## Public hostnames

Cloudflare Tunnel routes are stored in `charts/cloudflared/values.yaml`.
Changing the generated ConfigMap changes its pod-template checksum and rolls
cloudflared automatically. Keep hostnames stable and named for the service they
provide.
