from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api import agent, incidents, memories, remediation, replay, sessions
from backend.db.database import init_db
from backend.db.seed import seed_demo
from backend.db.schema import User
from backend.db.database import SessionLocal


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    with SessionLocal() as db:
        empty = db.get(User, "U001") is None
    if empty:
        seed_demo()
    yield


app = FastAPI(title="RecallGuard", version="0.1.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
                   allow_methods=["*"], allow_headers=["*"])
for r in (sessions, memories, agent, incidents, replay, remediation):
    app.include_router(r.router)


@app.get("/api/health")
def health():
    return {"ok": True}
