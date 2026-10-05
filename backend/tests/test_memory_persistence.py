from backend.tests.conftest import make_incident


def test_memory_persists_across_sessions(client):
    s3 = client.post("/api/session").json()["session_id"]
    assert s3 not in ("S001", "S002")
    ids = [m["id"] for m in client.get("/api/memories").json()]
    assert ids == ["M001", "M002", "M003"]
    d = client.post("/api/agent/decide", json={"session_id": s3, "message": "Book Tokyo"}).json()
    assert d["memory_ids_available"] == ["M001", "M002", "M003"]


def test_new_memory_gets_sequential_id(client):
    m = client.post("/api/memory", json={"content": "Window seat please."}).json()
    assert m["id"] == "M004" and m["status"] == "ACTIVE"


def test_snapshot_contains_exact_memory_ids(client):
    d, inc = make_incident(client)
    assert inc["snapshot"]["memory_ids"] == ["M001", "M002", "M003"]
    assert inc["snapshot"]["prompt_version"] == "v1"
    assert inc["incident_type"] == "CONSTRAINT_VIOLATION" and d["selected_option_id"] == "FLIGHT_A"


def test_nebius_response_schema():
    import pytest
    from backend.agent.decision_schema import DecisionValidationError, parse_decision
    good = '{"selected_option_id":"FLIGHT_A","decision_factors":[],"memory_ids_used":["M001"],"confidence":0.5,"summary":"x"}'
    assert parse_decision(good, {"FLIGHT_A"}, {"M001"}).selected_option_id == "FLIGHT_A"
    for bad in [good.replace("FLIGHT_A", "FLIGHT_Z"), good.replace('"M001"', '"M999"'),
                good.replace("0.5", "1.5"), "not json"]:
        with pytest.raises(DecisionValidationError):
            parse_decision(bad, {"FLIGHT_A"}, {"M001"})
