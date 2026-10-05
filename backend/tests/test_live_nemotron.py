"""Real Nemotron via Nebius Token Factory. Run: RUN_LIVE=1 uv run pytest -m live -s"""
import os

import pytest

from backend.nebius.client import get_llm
from backend.tests.conftest import make_incident

pytestmark = [pytest.mark.live,
              pytest.mark.skipif(os.environ.get("RUN_LIVE") != "1", reason="set RUN_LIVE=1")]


@pytest.fixture()
def client():  # real model: no dependency override
    from fastapi.testclient import TestClient
    from backend.db.seed import seed_demo
    from backend.main import app
    app.dependency_overrides.clear()
    seed_demo()
    with TestClient(app) as c:
        yield c


def test_full_loop_with_real_nemotron(client):
    d, inc = make_incident(client)
    iid = inc["incident_id"]
    assert d["selected_option_id"] == "FLIGHT_A", d
    rep = client.post(f"/api/incidents/{iid}/replay").json()
    assert rep["reproduced"], rep  # Gate 1
    client.post(f"/api/incidents/{iid}/counterfactual")
    a = {x["memory_id"]: x for x in client.get(f"/api/incidents/{iid}/attribution").json()["ranked"]}
    print({k: (v["counterfactual_action"], v["attribution_score"], v["status"]) for k, v in a.items()})
    assert a["M001"]["influence"] == "HIGH" and a["M001"]["counterfactual_action"] != "FLIGHT_A"  # Gate 2
    assert a["M002"]["influence"] == "LOW" and a["M003"]["influence"] == "LOW"
    client.post("/api/memories/M001/quarantine")
    v = client.post(f"/api/incidents/{iid}/verify").json()  # Gate 3
    assert v["changed"] and "M001" not in v["decision"]["memory_ids_available"], v
