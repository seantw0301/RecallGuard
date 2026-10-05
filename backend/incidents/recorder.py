import re

from sqlalchemy.orm import Session

from backend.agent.prompts import PROMPT_VERSION, SYSTEM_PROMPT_HASH
from backend.db.schema import Decision, DecisionRequest, Incident, ReplaySnapshot, next_id
from backend.events import publish

_AVOID = re.compile(r"\b(avoid|dislike|hate|no)\b", re.I)


def detect_violation(decision: Decision, options: list[dict]) -> str | None:
    """Demo heuristic: chosen option has an overnight layover while an ACTIVE memory says to avoid it."""
    chosen = next((o for o in options if o["id"] == decision.selected_option_id), None)
    if not chosen or not chosen.get("overnight_layover"):
        return None
    for m in decision.memories_json:
        if "overnight" in m["content"].lower() and _AVOID.search(m["content"]):
            return f"{chosen['label']} has an overnight layover, but {m['id']} says: \"{m['content']}\""
    return None


def create_incident(db: Session, decision: Decision, reason: str | None = None) -> tuple[Incident, ReplaySnapshot]:
    req = db.get(DecisionRequest, decision.request_id)
    violation = detect_violation(decision, req.options_json)
    inc = Incident(
        id=next_id(db, Incident, "I"), decision_id=decision.id,
        incident_type="CONSTRAINT_VIOLATION" if violation else "USER_REPORTED",
        description=violation or reason or "User reported an unexpected action.")
    db.add(inc)
    db.flush()
    snap = ReplaySnapshot(
        id=next_id(db, ReplaySnapshot, "SN"), incident_id=inc.id, user_message=req.user_message,
        options_json=req.options_json, memory_ids=[m["id"] for m in decision.memories_json],
        memories_json=decision.memories_json, model_name=decision.model_name,
        prompt_version=PROMPT_VERSION, system_prompt_hash=SYSTEM_PROMPT_HASH)
    db.add(snap)
    db.commit()
    publish(db, "incident.opened", inc.id, {"decision_id": decision.id})
    publish(db, "snapshot.created", inc.id, {"snapshot_id": snap.id, "memory_ids": snap.memory_ids})
    return inc, snap
