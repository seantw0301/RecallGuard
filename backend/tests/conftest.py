import json
import os
import tempfile

os.environ["RECALLGUARD_DB_URL"] = f"sqlite:///{tempfile.mkdtemp()}/test.db"

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from backend.db.seed import seed_demo  # noqa: E402
from backend.main import app  # noqa: E402
from backend.nebius.client import get_llm  # noqa: E402
from backend.nebius.models import ChatResult  # noqa: E402


class FakeLLM:
    """TEST DOUBLE ONLY: stands in for Nemotron so the pipeline is testable offline.
    Real-model behaviour is verified by test_live_nemotron.py (RUN_LIVE=1)."""

    def __init__(self):
        self.calls = 0
        self.script: list[str] | None = None  # optional forced outputs (for instability tests)

    def chat_json(self, messages):
        self.calls += 1
        text = messages[0]["content"]
        mems = json.loads(text.split("Relevant user memories:\n")[1].split("\n\nSelect exactly")[0]) \
            if "(none)" not in text.split("Relevant user memories:\n")[1][:8] else {}
        blob = " ".join(mems.values()).lower()
        if self.script:
            pick = self.script[(self.calls - 1) % len(self.script)]
        elif "cheapest" in blob:
            pick = "FLIGHT_A"
        elif "overnight" in blob:
            pick = "FLIGHT_C"
        else:
            pick = "FLIGHT_B"
        used = [k for k in mems if "cheapest" in mems[k].lower()] or list(mems)[:1]
        return ChatResult(json.dumps({"selected_option_id": pick, "decision_factors": ["fake"],
                                      "memory_ids_used": used, "confidence": 0.9, "summary": "fake"}),
                          "fake-model", 5)


@pytest.fixture()
def llm():
    return FakeLLM()


@pytest.fixture()
def client(llm):
    app.dependency_overrides[get_llm] = lambda: llm
    seed_demo()
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


def make_incident(client, message="Book me a flight to Tokyo next Friday."):
    d = client.post("/api/agent/decide", json={"session_id": "S002", "message": message}).json()
    inc = client.post("/api/incidents", json={"decision_id": d["decision_id"]}).json()
    return d, inc
