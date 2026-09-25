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

Before pushing a change, render and validate the affected path:

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

Pin deployed versions in Git. Flux image automation updates only fields with an
`$imagepolicy` marker using the bounded policies in `image-policies.yaml`.
The `*-latest` policies in `latest-image-policies.yaml` discover newer stable
image releases across minor and major versions; they have no setters and never
change the deployed image. An update alert reports new image selections.
OCI chart sources and HelmReleases keep bounded semver ranges for compatible
automatic upgrades. A broad chart range would install a new major immediately,
so do not widen it without checking compatibility and a verified backup for
stateful or infrastructure components. Promote a major by updating the Git
range after the checks; Flux then reconciles the new version.

Review ImagePolicy readiness after adding an automated dependency:

```bash
flux get images all -A
```

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
