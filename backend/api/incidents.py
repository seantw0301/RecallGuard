from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.agent.decision_schema import DecisionValidationError
from backend.agent.personal_agent import decide, load_options
from backend.api import serializers as ser
from backend.db.database import get_db
from backend.db.schema import Decision, DecisionRequest, Event, Incident, ReplaySnapshot
from backend.events import publish
from backend.incidents.recorder import create_incident, detect_violation
from backend.nebius.client import get_llm
from backend.nebius.models import NebiusError

router = APIRouter(prefix="/api")


class IncidentIn(BaseModel):
    decision_id: str
    reason: str | None = None


def get_incident(db: Session, incident_id: str) -> Incident:
    inc = db.get(Incident, incident_id)
    if inc is None:
        raise HTTPException(404, "incident not found")
    return inc


def get_snapshot(db: Session, incident_id: str) -> ReplaySnapshot:
    return db.scalars(select(ReplaySnapshot).where(ReplaySnapshot.incident_id == incident_id)).one()


@router.post("/incidents")
def report_incident(body: IncidentIn, db: Session = Depends(get_db)):
    dec = db.get(Decision, body.decision_id)
    if dec is None:
        raise HTTPException(404, "decision not found")
    inc, snap = create_incident(db, dec, body.reason)
    return {**ser.incident(inc), "snapshot": ser.snapshot(snap)}


@router.get("/incidents/{incident_id}")
def read_incident(incident_id: str, db: Session = Depends(get_db)):
    inc = get_incident(db, incident_id)
    dec = db.get(Decision, inc.decision_id)
    req = db.get(DecisionRequest, dec.request_id)
    return {**ser.incident(inc), "snapshot": ser.snapshot(get_snapshot(db, inc.id)),
            "decision": ser.decision(dec, req.options_json, detect_violation(dec, req.options_json))}


@router.post("/incidents/{incident_id}/verify")
def verify(incident_id: str, db: Session = Depends(get_db), llm=Depends(get_llm)):
    """Re-run the original request with current ACTIVE memories; RESOLVED if the action changed."""
    inc = get_incident(db, incident_id)
    orig = db.get(Decision, inc.decision_id)
    req = db.get(DecisionRequest, orig.request_id)
    try:
        new = decide(db, llm, req.session_id, req.user_message, kind="VERIFICATION")
    except (NebiusError, DecisionValidationError) as e:
        raise HTTPException(502, str(e))
    changed = new.selected_option_id != orig.selected_option_id
    if changed:
        inc.status = "RESOLVED"
        db.commit()
    publish(db, "verification.completed", inc.id, {"changed": changed, "action": new.selected_option_id})
    return {"changed": changed, "original_action": orig.selected_option_id,
            "incident_status": inc.status,
            "decision": ser.decision(new, req.options_json, detect_violation(new, req.options_json))}


@router.get("/incidents/{incident_id}/events")
def incident_events(incident_id: str, db: Session = Depends(get_db)):
    rows = db.scalars(select(Event).where(Event.incident_id == incident_id).order_by(Event.id))
    return [{"type": e.type, "payload": e.payload_json, "occurred_at": e.created_at.isoformat()} for e in rows]
