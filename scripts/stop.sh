#!/usr/bin/env bash
cd "$(dirname "$0")/.."
for n in backend frontend; do
  [ -f artifacts/$n.pid ] && kill "$(cat artifacts/$n.pid)" 2>/dev/null; rm -f artifacts/$n.pid
done
pkill -f "next dev -p 3000" 2>/dev/null; pkill -f "uvicorn backend.main" 2>/dev/null
echo stopped
