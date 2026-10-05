from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.config import DEMO_USER_ID
from backend.db.database import get_db
from backend.db.schema import ChatSession, User, next_id
from backend.db.seed import seed_demo

router = APIRouter(prefix="/api")


@router.post("/session")
def create_session(db: Session = Depends(get_db)):
    if db.get(User, DEMO_USER_ID) is None:
        db.add(User(id=DEMO_USER_ID, name="Demo User"))
    s = ChatSession(id=next_id(db, ChatSession, "S"), user_id=DEMO_USER_ID)
    db.add(s)
    db.commit()
    return {"session_id": s.id, "user_id": s.user_id}


@router.post("/demo/reset")
def demo_reset():
    return {"ok": True, **seed_demo()}
