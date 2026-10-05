from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.db.schema import Memory, next_id

ALLOWED = {
    "ACTIVE": {"QUARANTINED", "REVOKED"},
    "QUARANTINED": {"ACTIVE", "REVOKED"},
    "REVOKED": set(),
}


class InvalidTransition(Exception):
    pass


def create_memory(db: Session, user_id: str, content: str, type_: str = "preference",
                  session_id: str | None = None, memory_id: str | None = None) -> Memory:
    m = Memory(id=memory_id or next_id(db, Memory, "M"), user_id=user_id, type=type_,
               content=content, status="ACTIVE", source_session_id=session_id)
    db.add(m)
    db.commit()
    return m


def list_memories(db: Session, user_id: str, status: str | None = None) -> list[Memory]:
    q = select(Memory).where(Memory.user_id == user_id).order_by(Memory.id)
    if status:
        q = q.where(Memory.status == status)
    return list(db.scalars(q))


def set_status(db: Session, memory_id: str, new_status: str) -> Memory | None:
    m = db.get(Memory, memory_id)
    if m is None:
        return None
    if new_status not in ALLOWED[m.status]:
        raise InvalidTransition(f"{m.status} -> {new_status}")
    m.status = new_status
    db.commit()
    return m
