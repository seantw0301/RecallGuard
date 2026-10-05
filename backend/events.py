"""In-process event log (audit trail). Published after the DB state change is committed."""
from sqlalchemy.orm import Session

from backend.db.schema import Event


def publish(db: Session, type_: str, incident_id: str | None = None, payload: dict | None = None) -> None:
    db.add(Event(type=type_, incident_id=incident_id, payload_json=payload or {}))
    db.commit()
