from sqlalchemy.orm import Session

from backend.memory.repository import list_memories


def select_active(db: Session, user_id: str) -> list[dict]:
    """ACTIVE memories only, stable order. QUARANTINED / REVOKED never reach the model."""
    return [{"id": m.id, "content": m.content} for m in list_memories(db, user_id, "ACTIVE")]
