from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.api import serializers as ser
from backend.config import DEMO_USER_ID
from backend.db.database import get_db
from backend.events import publish
from backend.memory import repository as repo

router = APIRouter(prefix="/api")


class MemoryIn(BaseModel):
    content: str
    type: str = "preference"
    session_id: str | None = None


@router.post("/memory")
def create_memory(body: MemoryIn, db: Session = Depends(get_db)):
    m = repo.create_memory(db, DEMO_USER_ID, body.content, body.type, body.session_id)
    publish(db, "memory.created", None, {"memory_id": m.id})
    return ser.memory(m)


@router.get("/memories")
def list_memories(status: str | None = None, db: Session = Depends(get_db)):
    return [ser.memory(m) for m in repo.list_memories(db, DEMO_USER_ID, status)]
