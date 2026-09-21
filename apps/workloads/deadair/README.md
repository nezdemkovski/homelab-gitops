# Dead Air

One station replica with bundled CPU TTS, external CNPG PostgreSQL and ephemeral Redis sessions.
Image 0.24.0 is pinned by digest. Access starts privately with `kubectl -n deadair port-forward svc/deadair 8080:80`; open http://localhost:8080.
No public DNS or tunnel route is created. The upstream stream has no authentication.

## Rollout

Merge only the two AppProject allowlist files first and verify homelab-root sync.
Then provision the `deadair` 1Password item and merge workload files.
Required fields: DATABASE_USER=deadair, DATABASE_PASSWORD, KMS_LOCAL_ROOT_KEY (32 random bytes in hex), AUTHENTICATION_SESSION_JWT_PRIVATE_KEY (base64 RSA PEM).
Store the xAI API key separately in 1Password; it is configured through the station's encrypted plugin settings, not an unsupported environment variable.

In Settings / Plugins / LLM, add provider `xai`, kind `openai-compat`, base URL `https://api.x.ai/v1`, and its API key. Grant the plugin access to api.x.ai. Select an available text model under Settings / Words and test a presenter break before scheduling it.
Authorize the music provider separately. First administrator registration is performed while access is private.

CNPG has daily object-store backups; `/data` PVC is retained and needs a filesystem backup before upgrades. Redis loss signs users out. Cache is node-bound local-path storage; set a track cache limit in the console. CPU TTS throughput and memory limits require a real playback trial.
