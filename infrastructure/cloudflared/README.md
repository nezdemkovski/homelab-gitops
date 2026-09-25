# Cloudflared

Flux reconciles cloudflared after Cilium. Public routes are declared in
`charts/cloudflared/values.yaml`; tunnel credentials come from 1Password
through External Secrets.

The Deployment pod template includes a checksum of the generated ConfigMap, so
changing a route rolls both replicas automatically. After route changes, wait
for both replicas and tunnel connections, then test every affected hostname.
