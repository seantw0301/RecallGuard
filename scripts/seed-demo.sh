#!/usr/bin/env bash
# Reset DB to deterministic demo seed (backend must be running).
curl -sf -X POST localhost:8000/api/demo/reset && echo
