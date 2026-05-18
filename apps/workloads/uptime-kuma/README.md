# Uptime Kuma

Uptime Kuma runs from plain Kubernetes manifests because the upstream project
does not publish an official Helm chart.

The image version is pinned in `deployment.yaml`:

```text
louislam/uptime-kuma:2.3.2
```

Data is stored in:

```text
uptime-kuma/uptime-kuma-data
```

The migrated Helios data came from:

```text
ssh yuri@10.77.77.134
/home/yuri/appdata/uptime-kuma
```

Uptime Kuma stores its SQLite database and app data under `/app/data`. Keep the
old Helios data until the Kubernetes instance is verified.

Public hostnames and Cloudflare Tunnel ingress rules are stored in 1Password,
not in Git.
