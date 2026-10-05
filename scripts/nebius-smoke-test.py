#!/usr/bin/env python3
"""Phase 0 / Gate 0: call Nemotron via Nebius Token Factory, validate decision JSON."""
import json, os, sys, time, urllib.request
from pathlib import Path

env = Path(__file__).resolve().parent.parent / ".env"
if env.exists():
    for line in env.read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

key, model, base = (os.environ.get(k) for k in ("NEBIUS_API_KEY", "NEBIUS_MODEL", "NEBIUS_BASE_URL"))
if not (key and model and base):
    sys.exit("FAIL: set NEBIUS_API_KEY / NEBIUS_MODEL / NEBIUS_BASE_URL")

OPTIONS = {"FLIGHT_A": "$320, 2 stops, overnight layover",
           "FLIGHT_B": "$390, direct, daytime",
           "FLIGHT_C": "$355, 1 stop, no overnight layover"}
MEMORIES = {"M001": "User usually prefers cheaper flights.",
            "M002": "Avoid overnight layovers.",
            "M003": "Economy class is fine."}
prompt = (
    "You are a personal assistant.\n\nUser request:\nBook me a flight to Tokyo next Friday.\n\n"
    f"Available options:\n{json.dumps(OPTIONS, indent=1)}\n\n"
    f"Relevant user memories:\n{json.dumps(MEMORIES, indent=1)}\n\n"
    "Select exactly one option. Return JSON only with keys: selected_option_id, "
    "decision_factors (list of str), memory_ids_used (list of str), confidence (0-1), summary."
)
body = {"model": model, "temperature": 0, "max_tokens": 1500,
        "messages": [{"role": "user", "content": prompt}],
        "response_format": {"type": "json_object"}}
req = urllib.request.Request(base.rstrip("/") + "/chat/completions", json.dumps(body).encode(),
                             {"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
t = time.time()
try:
    resp = json.load(urllib.request.urlopen(req, timeout=60))
except Exception as e:
    sys.exit(f"FAIL: request error: {e}")
ms = int((time.time() - t) * 1000)
text = resp["choices"][0]["message"]["content"]
try:
    out = json.loads(text[text.index("{"): text.rindex("}") + 1])
    assert out["selected_option_id"] in OPTIONS
    assert set(out["memory_ids_used"]) <= set(MEMORIES)
    assert 0 <= float(out["confidence"]) <= 1
    assert isinstance(out["decision_factors"], list) and out["summary"]
except Exception as e:
    sys.exit(f"FAIL: invalid output ({e!r}): {text[:400]}")
print(f"PASS model={resp.get('model', model)} latency={ms}ms")
print(json.dumps(out, indent=1))
