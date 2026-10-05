# Deployment

| Item | Value |
|---|---|
| Host | `ssh -p 1122 root@192.168.1.200` (Ubuntu, BT panel + nginx) |
| Dir | `/www/wwwroot/recallguard.jxdtw.com` (owner `www`) |
| URL | https://recallguard.jxdtw.com (cert managed by the panel) |
| Backend | systemd `recallguard-backend` → uvicorn `127.0.0.1:18000` |
| Frontend | systemd `recallguard-frontend` → `next start 127.0.0.1:18001` |
| DB | SQLite `backend/recallguard.db` |
| Secrets | `.env` in the dir (`root:www`, mode 640; blocked by nginx; not in git) |

## Routing

nginx extension file `/www/server/panel/vhost/nginx/extension/recallguard.jxdtw.com/app.conf`:

- `^~ /api/` → `:18000` (read timeout 180 s — replays take ~10 s)
- `^~ /` → `:18001`
- `^~ /.well-known/` → webroot (cert renewal)

`^~` is required: the panel vhost has a catch-all `location ~ .*\.(js|css)?$` that would otherwise win.

## Update

```bash
scripts/deploy.sh      # rsync → uv sync → npm ci/build → restart → health check
```

## Ops

```bash
systemctl status recallguard-backend recallguard-frontend
journalctl -u recallguard-backend -f
curl -X POST https://recallguard.jxdtw.com/api/demo/reset   # fresh demo state
```

## Notes / risks

- Public demo, no auth: anyone can call `/api/agent/decide` (spends Nebius quota) and `/api/demo/reset`. Add basic auth or an nginx `limit_req` zone if exposed beyond judging.
- One shared SQLite demo state: concurrent visitors share memories/incidents.
- E2E check against production: `BASE_URL=https://recallguard.jxdtw.com npx playwright test` (in `demo/`).
