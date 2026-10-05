from backend.tests.conftest import make_incident


def _attr(client, iid):
    return {a["memory_id"]: a for a in client.get(f"/api/incidents/{iid}/attribution").json()["ranked"]}


def test_original_replay_reproduces_action(client, llm):
    d, inc = make_incident(client)
    r = client.post(f"/api/incidents/{inc['incident_id']}/replay").json()
    assert r["reproduced"] and r["stability"] == "STABLE" and r["action"] == d["selected_option_id"]
    assert len(r["runs"]) == 3


def test_remove_m001_changes_action_and_m002_does_not(client):
    _, inc = make_incident(client)
    iid = inc["incident_id"]
    client.post(f"/api/incidents/{iid}/replay")
    out = client.post(f"/api/incidents/{iid}/counterfactual").json()
    a = _attr(client, iid)
    assert a["M001"]["action_changed"] and a["M001"]["attribution_score"] == 1.0 and a["M001"]["influence"] == "HIGH"
    assert not a["M002"]["action_changed"] and a["M002"]["attribution_score"] == 0.0 and a["M002"]["influence"] == "LOW"
    assert not a["M003"]["action_changed"]
    assert out["attribution"][0]["memory_id"] == "M001" and out["incident_status"] == "REMEDIATION_PENDING"


def test_unstable_replay_flag_blocks_attribution(client, llm):
    _, inc = make_incident(client)
    iid = inc["incident_id"]
    llm.script = ["FLIGHT_A", "FLIGHT_B", "FLIGHT_A"]
    r = client.post(f"/api/incidents/{iid}/replay").json()
    assert r["stability"] == "UNSTABLE" and not r["reproduced"] and r["incident_status"] == "REPLAY_UNSTABLE"
    assert client.post(f"/api/incidents/{iid}/counterfactual").status_code == 409


def test_no_influence_found_when_nothing_changes(client, llm):
    _, inc = make_incident(client)
    iid = inc["incident_id"]
    client.post(f"/api/incidents/{iid}/replay")
    llm.script = ["FLIGHT_A"]
    out = client.post(f"/api/incidents/{iid}/counterfactual").json()
    assert out["incident_status"] == "NO_INFLUENCE_FOUND"  # Gate 2 reported, not faked


def test_incident_trace(client):
    _, inc = make_incident(client)
    iid = inc["incident_id"]
    client.post(f"/api/incidents/{iid}/replay")
    client.post(f"/api/incidents/{iid}/counterfactual")
    types = [e["type"] for e in client.get(f"/api/incidents/{iid}/events").json()]
    assert types[:2] == ["incident.opened", "snapshot.created"]
    assert "replay.original.verified" in types and "attribution.computed" in types
    full = client.get(f"/api/incidents/{iid}").json()
    assert full["decision"]["model_name"] == "fake-model" and full["snapshot"]["system_prompt_hash"]
