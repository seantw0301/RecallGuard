#!/usr/bin/env bash
# One-shot install: Python 3.12 env (uv), frontend deps, demo (Playwright) deps.
set -euo pipefail
cd "$(dirname "$0")/.."
command -v uv >/dev/null || { echo "install uv first: https://docs.astral.sh/uv/"; exit 1; }
[ -f .env ] || { cp .env.example .env; echo "Created .env — fill NEBIUS_API_KEY"; }
uv sync
(cd frontend && npm install)
(cd demo && npm install && npx playwright install chromium ffmpeg)
echo "Done. Next: scripts/start.sh"
