import json

from backend.config import DATA_DIR, DEMO_USER_ID
from backend.db.database import SessionLocal, reset_db
from backend.db.schema import ChatSession, Memory, User


def seed_demo() -> dict:
    """Deterministic demo state: Demo User, Session 1 (memories) and Session 2 (action)."""
    seed = json.loads((DATA_DIR / "demo-seed.json").read_text())
    reset_db()
    with SessionLocal() as db:
        db.add(User(id=seed["user"]["id"], name=seed["user"]["name"]))
        db.add_all([ChatSession(id=seed["session1"], user_id=DEMO_USER_ID),
                    ChatSession(id=seed["session2"], user_id=DEMO_USER_ID)])
        db.flush()
        db.add_all([Memory(id=m["id"], user_id=DEMO_USER_ID, type=m["type"], content=m["content"],
                           status="ACTIVE", source_session_id=seed["session1"]) for m in seed["memories"]])
        db.commit()
    return {"session1": seed["session1"], "session2": seed["session2"],
            "demo_request": seed["demo_request"], "user_id": DEMO_USER_ID}
