#!/usr/bin/env bash
# Record the product demo with a neural narrator (Kokoro, local) → artifacts/recallguard-demo-audio.mp4
# Needs KOKORO_ENV (see docs/demo-voice.md). Starts the stack if needed.
set -euo pipefail
cd "$(dirname "$0")/.."
KOKORO_ENV="${KOKORO_ENV:-/Users/seantw/case2026/Claude/IntentChain/video/tts-env}"
curl -sf localhost:3000 >/dev/null && curl -sf localhost:8000/api/health >/dev/null || scripts/start.sh
mkdir -p artifacts
"$KOKORO_ENV/bin/python" -I scripts/voice.py --clips demo/narration.json artifacts/audio >/dev/null
(cd demo && npx playwright test)
python3 scripts/mux-audio.py
echo "Video: artifacts/recallguard-demo.webm (silent) · artifacts/recallguard-demo-audio.mp4 (narrated)"
