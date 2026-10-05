#!/usr/bin/env bash
# Record the full demo to artifacts/recallguard-demo.webm (starts the stack if needed).
set -euo pipefail
cd "$(dirname "$0")/.."
curl -sf localhost:3000 >/dev/null || scripts/start.sh
(cd demo && npx playwright test)
echo "Video: artifacts/recallguard-demo.webm"
