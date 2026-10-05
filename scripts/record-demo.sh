#!/usr/bin/env bash
# Record the demo: silent webm + narrated mp4 (macOS `say` voice). Starts the stack if needed.
set -euo pipefail
cd "$(dirname "$0")/.."
curl -sf localhost:3000 >/dev/null && curl -sf localhost:8000/api/health >/dev/null || scripts/start.sh
python3 scripts/narrate.py >/dev/null
(cd demo && npx playwright test)
python3 scripts/mux-audio.py
echo "Video: artifacts/recallguard-demo.webm (silent) · artifacts/recallguard-demo-audio.mp4 (narrated)"
