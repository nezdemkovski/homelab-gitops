# Cloudflared Flux handoff

This directory is intentionally referenced by a suspended cluster
`Kustomization` and depends on the Cilium Kustomization.

The HelmRelease uses the existing release name and namespace and enables Helm
take-ownership because the Argo-rendered chart has no Helm release storage.
The chart keeps routes for the retired Actual Budget, FNPC, and Nezdemos
services absent. The first Flux reconciliation rolls both tunnel replicas
through the new config revision so the running tunnel process reloads the
Git-managed ingress list.

Activate this Kustomization only after Cilium is Ready under Flux. Disable Argo
automation and remove the cloudflared Application finalizer first, then verify
that the Deployment, ConfigMap, and ExternalSecret retain their UIDs. Wait for
both replicas and tunnel connections to recover, and test every retained public
hostname before deleting the Argo Application.
