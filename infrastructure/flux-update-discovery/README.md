# Helm chart version discovery

These Flux sources select the latest stable chart versions with `*` but have no
HelmRelease consumers. They download chart artifacts for inspection and emit
source events when a newer artifact appears; they do not install or upgrade
anything. The live HelmRelease and OCIRepository ranges remain in their app or
infrastructure directories.

The manifests were generated with `flux create source chart` and
`flux create source oci`. When adding a chart source, also add it to the
`telegram-available-charts` Alert. A major stateful or infrastructure upgrade
requires a compatibility review and verified backup before widening the live
range in Git.
