from backend.db import schema as s


def memory(m: s.Memory) -> dict:
    return {"id": m.id, "type": m.type, "content": m.content, "status": m.status,
            "source_session_id": m.source_session_id, "created_at": m.created_at.isoformat()}


def decision(d: s.Decision, options: list[dict] | None = None, violation: str | None = None) -> dict:
    return {"decision_id": d.id, "request_id": d.request_id, "kind": d.kind,
            "selected_option_id": d.selected_option_id, "summary": d.reasoning_summary,
            "decision_factors": d.decision_factors_json,
            "memory_ids_used": d.memory_ids_used_json,  # model-reported evidence
            "memory_ids_available": [m["id"] for m in d.memories_json],
            "confidence": d.confidence, "model_name": d.model_name, "model_provider": d.model_provider,
            "latency_ms": d.latency_ms, "options": options, "violation": violation}


def incident(i: s.Incident) -> dict:
    return {"incident_id": i.id, "decision_id": i.decision_id, "incident_type": i.incident_type,
            "description": i.description, "status": i.status, "original_stability": i.original_stability,
            "original_reproduced": i.original_reproduced, "created_at": i.created_at.isoformat()}


def snapshot(sn: s.ReplaySnapshot) -> dict:
    return {"snapshot_id": sn.id, "incident_id": sn.incident_id, "user_message": sn.user_message,
            "memory_ids": sn.memory_ids, "memories": sn.memories_json, "model_name": sn.model_name,
            "prompt_version": sn.prompt_version, "system_prompt_hash": sn.system_prompt_hash}


def run(r: s.ReplayRun) -> dict:
    return {"id": r.id, "run_type": r.run_type, "run_index": r.run_index,
            "removed_memory_id": r.removed_memory_id, "selected_option_id": r.selected_option_id,
            "summary": r.reasoning_summary, "memory_ids_used": r.memory_ids_used_json, "status": r.status,
            "error": r.error, "model_name": r.model_name, "latency_ms": r.latency_ms}


def attribution(a: s.AttributionResult) -> dict:
    return {"memory_id": a.memory_id, "original_action": a.original_action,
            "counterfactual_action": a.counterfactual_action, "action_changed": a.action_changed,
            "attribution_score": a.attribution_score, "influence": a.influence, "status": a.status,
            "changed_runs": a.changed_runs, "total_runs": a.total_runs}
