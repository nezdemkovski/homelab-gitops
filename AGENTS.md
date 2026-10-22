# AGENTS.md

Operational rules for this Talos/Flux homelab. Start with the current Git state,
affected manifests and live resource status; do not infer deployment state from
an old release or a previous run.

## GitOps workflow

- `master` is the source of truth for the `homelab` cluster. Flux is the only
  deployment reconciler. Bootstrap resources are in
  `clusters/homelab/flux-system`; component Kustomizations are in
  `clusters/homelab/`; workloads are in `apps/`; shared services are in
  `infrastructure/`; local charts are in `charts/`.
- Keep one Kustomization per independently operated component, with
  `spec.dependsOn` for ordering. Prefer `flux create ... --export` for new Flux
  resources. Commit durable resources instead of applying them by hand.
- Use global `~/.kube/config` with explicit context `admin@homelab`, and
  `~/.talos/config` with context `homelab`. Keep files `0600`, outside the repo;
  preserve other contexts when restoring. Recovery attachments are in the
  `kubernetes` and `talos` 1Password notes.

From the repo root, render the selected Kustomization's **`spec.path`** as
`<manifest-path>` below. Do not use the directory holding its Flux definition
unless that is the resource's actual target path.

```bash
flux --context admin@homelab build kustomization <name> --path <manifest-path> \
  --kustomization-file ./clusters/homelab/<name>.yaml --dry-run --in-memory-build
git diff --check
```

Offline builds skip Secret/ConfigMap-backed substitutions. For changed charts,
also render Helm templates with the actual release name, namespace and values;
a rendered HelmRelease alone does not validate chart output.

After pushing, reconcile and verify the expected revision and Ready conditions:

```bash
flux --context admin@homelab reconcile source git flux-system
flux --context admin@homelab reconcile kustomization <name> --with-source
flux --context admin@homelab get kustomizations
flux --context admin@homelab get helmreleases -A
```

Check the affected workload and real service behavior as well. Limit Flux
suspension to a bounded maintenance window, resume afterward, and record durable
live changes in Git. Talos OS and Kubernetes upgrades are separate operations;
Flux does not upgrade the node OS.

## Released-client compatibility before deployment (mandatory)

Playdamnit has released native clients. Apply this rule to Playdamnit and every
other workload serving supported released applications: **do not deploy an API
change that breaks those installed clients.** Read the product repository's
`AGENTS.md` and its released-client compatibility rules before changing release
pins, routes, authentication configuration or other API-affecting infrastructure.

- Before an API-affecting rollout, verify compatibility evidence for the exact
  image/source revision against supported released client versions and commits.
  Require checks using original shipped decoders/models and affected old request
  shapes; a green build with a regenerated SDK is insufficient.
- Preserve endpoint paths, response and request shapes, types/nullability, enum
  cases, status/error behavior, authentication, defaults and business semantics.
  Routing, secret/configuration and dependency changes can break clients even
  when the OpenAPI document is unchanged.
- Deploy compatible server support before a new client depends on it. A web
  deployment or TestFlight upload does not update already-installed apps. Verify
  old client behavior against the deployed API and keep a compatible rollback.
- If a change cannot preserve the existing contract, keep the old version served
  and introduce a versioned contract. Do not deploy the incompatible change to an
  existing endpoint or retire support without explicit product-owner approval of
  the support and migration plan.

## Persistent data

- Set `kustomize.toolkit.fluxcd.io/prune: disabled` on namespaces containing
  persistent application data, Git-managed PVCs and CloudNativePG Clusters.
- Keep storage reclaim policies `Retain` and verified backups outside the node.
  `local-path` volumes are node-bound.
- Before removing, renaming or moving stateful resources, inspect PVC/PV bindings
  and verify a recent restorable backup. Never delete a namespace to reset or
  back up an application.

## Versions and dependency review

Pin exact chart versions, OCI `ref.tag` and image tags; own images include a
version and digest (`x.y.z@sha256:...`). Keep registry/repository beside the tag
so Renovate can detect it. Do not use semver ranges.

[Renovate configuration](.renovaterc.json5) groups updates by stack and labels
major/minor/patch/digest updates. The [Renovate workflow](.github/workflows/renovate.yaml)
runs hourly and proposes PRs; Renovate's own automerge is disabled.

[Dependency Review](.github/workflows/claude-renovate-review.yaml) reviews
same-repository Renovate PRs. Claude checks the full release range, upstream
changes behind wrapper charts/images and local consumers. It returns a verdict;
the [trusted finalizer](scripts/finalize-renovate-review.py) from `master` owns
labels, the comment and merging, and checks both head and base revisions.

- Uncertainty, relevant breaking changes, required migration, missing release
  notes or review failure require human investigation.
- All `type/major` PRs stay open for verified backup and human merge. Workflow
  changes also stay open: the merge token does not request `workflows` permission.
  PRs with 100 or more changed files require human review.
- The finalizer adds `review/approved` or `review/needs-human` and applicable
  `risk/breaking-change` / `risk/migration` labels. It merges only the approved,
  unchanged head that passes its gates. The comment separates Claude's verdict
  from the merge decision. A non-approval can leave the check green while the PR
  stays open; GitHub API or merge failures fail the job.

CI credentials (`RENOVATE_APP_CLIENT_ID`, `RENOVATE_APP_PRIVATE_KEY`, `GHCR_TOKEN`,
`CLAUDE_CODE_OAUTH_TOKEN`) belong in GitHub repository secrets, not 1Password.

## Secrets

Runtime secrets live in the `Homelab` 1Password vault and reach ESO through
1Password Connect and the `onepassword` ClusterSecretStore. Keep one Secure Note
per service, without tags; follow the [vault field conventions](infrastructure/onepassword-store/README.md).
Commit only ExternalSecret references, never generated Secrets, credentials,
client configs or tokens. Config recovery attachments are not runtime secrets.

After changing mappings, verify a fresh ExternalSecret sync and consumer
readiness. For reorganization without rotation, compare consumer Secret data via
hashes without displaying values; unchanged data needs no restart.

## Network and public routes

Cilium enforces deny-by-default workload policies. Add only required ingress and
egress for DNS, Kubernetes API, applications, databases, backups, monitoring and
tunnel traffic. Public internet egress excludes private ranges; LAN dependencies
such as `10.77.77.0/24` need a documented service-specific rule. Validate affected
connections after shared-policy changes.

Public routes are in `charts/cloudflared/values.yaml`. Keep hostnames stable and
named for the service. Route changes alter the ConfigMap checksum and roll the
tunnel pods; verify the rollout, Service backends, DNS and public response.
