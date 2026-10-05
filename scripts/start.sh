#!/usr/bin/env bash
# Start backend (:8000) and frontend (:3000) in the background. Logs in artifacts/logs.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p artifacts/logs
.venv/bin/uvicorn backend.main:app --port 8000 > artifacts/logs/backend.log 2>&1 &
echo $! > artifacts/backend.pid
ROOT=$PWD
(cd frontend && exec npx next dev -p 3000 > "$ROOT/artifacts/logs/frontend.log" 2>&1) &
echo $! > artifacts/frontend.pid
for i in $(seq 1 40); do
  curl -sf localhost:8000/api/health >/dev/null && curl -sf localhost:3000 >/dev/null && { echo "RecallGuard: http://localhost:3000"; exit 0; }
  sleep 1
done
echo "failed to start; see artifacts/logs"; exit 1
