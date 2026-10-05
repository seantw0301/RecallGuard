#!/usr/bin/env bash
# Deploy to the production host (idempotent). Server: ssh -p 1122 root@192.168.1.200
# Public URL: https://recallguard.jxdtw.com  ·  Dir: /www/wwwroot/recallguard.jxdtw.com
# First-time setup (systemd units + nginx proxy) is described in docs/deploy.md.
set -euo pipefail
cd "$(dirname "$0")/.."
HOST=root@192.168.1.200; SSH="ssh -p 1122"; D=/www/wwwroot/recallguard.jxdtw.com
rsync -az -e "$SSH" --exclude .git --exclude .venv --exclude node_modules --exclude artifacts --exclude .env \
  --exclude '*.db' --exclude .next --exclude __pycache__ --exclude demo --exclude .DS_Store --exclude .pytest_cache \
  ./ $HOST:$D/
$SSH $HOST "cd $D && uv sync --python 3.14 -q && cd frontend && npm ci --silent && npm run build >/dev/null \
  && chown -R www:www $D 2>/dev/null; systemctl restart recallguard-backend recallguard-frontend; sleep 3; curl -sf localhost:18000/api/health"
echo; curl -sf -o /dev/null -w "public: %{http_code}\n" https://recallguard.jxdtw.com/api/health
