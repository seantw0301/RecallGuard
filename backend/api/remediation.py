from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.api import serializers as ser
from backend.db.database import get_db
from backend.events import publish
from backend.memory import repository as repo

router = APIRouter(prefix="/api")


def _transition(db: Session, memory_id: str, status: str, event: str):
    try:
        m = repo.set_status(db, memory_id, status)
    except repo.InvalidTransition as e:
        raise HTTPException(409, str(e))
    if m is None:
        raise HTTPException(404, "memory not found")
    publish(db, event, None, {"memory_id": memory_id})
    return ser.memory(m)


@router.post("/memories/{memory_id}/quarantine")
def quarantine(memory_id: str, db: Session = Depends(get_db)):
    return _transition(db, memory_id, "QUARANTINED", "memory.quarantined")


@router.post("/memories/{memory_id}/restore")
def restore(memory_id: str, db: Session = Depends(get_db)):
    return _transition(db, memory_id, "ACTIVE", "memory.restored")


@router.post("/memories/{memory_id}/revoke")
def revoke(memory_id: str, db: Session = Depends(get_db)):
    return _transition(db, memory_id, "REVOKED", "memory.revoked")
