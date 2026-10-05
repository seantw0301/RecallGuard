from backend.tests.conftest import make_incident


def test_quarantined_memory_is_excluded(client):
    assert client.post("/api/memories/M001/quarantine").json()["status"] == "QUARANTINED"
    d = client.post("/api/agent/decide", json={"session_id": "S002", "message": "Tokyo"}).json()
    assert d["memory_ids_available"] == ["M002", "M003"]
    assert d["selected_option_id"] != "FLIGHT_A"


def test_quarantine_changes_future_behavior_and_resolves(client):
    d, inc = make_incident(client)
    iid = inc["incident_id"]
    client.post("/api/memories/M001/quarantine")
    v = client.post(f"/api/incidents/{iid}/verify").json()
    assert v["changed"] and v["original_action"] == "FLIGHT_A" and v["incident_status"] == "RESOLVED"
    assert "M001" not in v["decision"]["memory_ids_available"]


def test_snapshot_unaffected_by_later_quarantine(client):
    _, inc = make_incident(client)
    client.post("/api/memories/M001/quarantine")
    snap = client.get(f"/api/incidents/{inc['incident_id']}").json()["snapshot"]
    assert snap["memory_ids"] == ["M001", "M002", "M003"]
    assert client.post(f"/api/incidents/{inc['incident_id']}/replay").json()["reproduced"]


def test_state_transitions(client):
    assert client.post("/api/memories/M001/restore").status_code == 409
    client.post("/api/memories/M001/quarantine")
    assert client.post("/api/memories/M001/quarantine").status_code == 409
    assert client.post("/api/memories/M001/restore").json()["status"] == "ACTIVE"
    client.post("/api/memories/M001/revoke")
    assert client.post("/api/memories/M001/restore").status_code == 409
    assert client.post("/api/memories/M999/quarantine").status_code == 404
