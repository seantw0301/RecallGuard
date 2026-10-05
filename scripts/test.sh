#!/usr/bin/env bash
# Offline suite always; real-Nemotron suite when RUN_LIVE=1 (needs .env).
set -euo pipefail
cd "$(dirname "$0")/.."
.venv/bin/python -m pytest -q
[ "${RUN_LIVE:-}" = "1" ] && RUN_LIVE=1 .venv/bin/python -m pytest -m live -s -q || true
