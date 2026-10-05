from datetime import datetime, timezone

from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, Integer, String, Text, select
from sqlalchemy.orm import Mapped, Session, mapped_column

from backend.db.database import Base


def _now() -> datetime:
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now)


class ChatSession(Base):
    __tablename__ = "sessions"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now)


class Memory(Base):
    __tablename__ = "memories"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    type: Mapped[str] = mapped_column(String, default="preference")
    content: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String, default="ACTIVE")  # ACTIVE|QUARANTINED|REVOKED
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now)
    source_session_id: Mapped[str | None] = mapped_column(String, nullable=True)


class DecisionRequest(Base):
    __tablename__ = "decision_requests"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    session_id: Mapped[str] = mapped_column(ForeignKey("sessions.id"))
    user_message: Mapped[str] = mapped_column(Text)
    task_type: Mapped[str] = mapped_column(String, default="flight_booking")
    options_json: Mapped[list] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now)


class Decision(Base):
    __tablename__ = "decisions"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    request_id: Mapped[str] = mapped_column(ForeignKey("decision_requests.id"))
    kind: Mapped[str] = mapped_column(String, default="LIVE")  # LIVE|VERIFICATION
    selected_option_id: Mapped[str] = mapped_column(String)
    reasoning_summary: Mapped[str] = mapped_column(Text)
    decision_factors_json: Mapped[list] = mapped_column(JSON)
    memory_ids_used_json: Mapped[list] = mapped_column(JSON)  # model-reported, not proof
    memories_json: Mapped[list] = mapped_column(JSON)  # frozen memories supplied to model
    confidence: Mapped[float] = mapped_column(Float)
    model_name: Mapped[str] = mapped_column(String)
    model_provider: Mapped[str] = mapped_column(String, default="nebius")
    latency_ms: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now)


class Incident(Base):
    __tablename__ = "incidents"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    decision_id: Mapped[str] = mapped_column(ForeignKey("decisions.id"))
    incident_type: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String, default="OPEN")
    original_stability: Mapped[str | None] = mapped_column(String, nullable=True)
    original_reproduced: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now)


class ReplaySnapshot(Base):
    __tablename__ = "replay_snapshots"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    incident_id: Mapped[str] = mapped_column(ForeignKey("incidents.id"))
    user_message: Mapped[str] = mapped_column(Text)
    options_json: Mapped[list] = mapped_column(JSON)
    memory_ids: Mapped[list] = mapped_column(JSON)
    memories_json: Mapped[list] = mapped_column(JSON)
    model_name: Mapped[str] = mapped_column(String)
    prompt_version: Mapped[str] = mapped_column(String)
    system_prompt_hash: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now)


class ReplayRun(Base):
    __tablename__ = "replay_runs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    snapshot_id: Mapped[str] = mapped_column(ForeignKey("replay_snapshots.id"))
    run_type: Mapped[str] = mapped_column(String)  # ORIGINAL|REMOVE_MEMORY|MODIFY_MEMORY|NO_MEMORY
    run_index: Mapped[int] = mapped_column(Integer, default=0)
    removed_memory_id: Mapped[str | None] = mapped_column(String, nullable=True)
    modified_memory_id: Mapped[str | None] = mapped_column(String, nullable=True)
    selected_option_id: Mapped[str | None] = mapped_column(String, nullable=True)
    reasoning_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    decision_factors_json: Mapped[list] = mapped_column(JSON, default=list)
    memory_ids_used_json: Mapped[list] = mapped_column(JSON, default=list)
    status: Mapped[str] = mapped_column(String, default="COMPLETED")  # COMPLETED|INVALID|FAILED
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    model_name: Mapped[str | None] = mapped_column(String, nullable=True)
    latency_ms: Mapped[int] = mapped_column(Integer, default=0)
    attempts: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now)


class AttributionResult(Base):
    __tablename__ = "attribution_results"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    incident_id: Mapped[str] = mapped_column(ForeignKey("incidents.id"))
    memory_id: Mapped[str] = mapped_column(String)
    original_action: Mapped[str] = mapped_column(String)
    counterfactual_action: Mapped[str | None] = mapped_column(String, nullable=True)
    action_changed: Mapped[bool] = mapped_column(Boolean)
    attribution_score: Mapped[float] = mapped_column(Float)
    influence: Mapped[str] = mapped_column(String)  # HIGH|MEDIUM|LOW
    status: Mapped[str] = mapped_column(String)  # STABLE|UNSTABLE|INCOMPLETE
    changed_runs: Mapped[int] = mapped_column(Integer)
    total_runs: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now)


class Event(Base):
    __tablename__ = "events"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    type: Mapped[str] = mapped_column(String)
    incident_id: Mapped[str | None] = mapped_column(String, nullable=True)
    payload_json: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now)


def next_id(db: Session, model, prefix: str, width: int = 3) -> str:
    ids = db.scalars(select(model.id)).all()
    nums = [int(i[len(prefix):]) for i in ids if i.startswith(prefix) and i[len(prefix):].isdigit()]
    return f"{prefix}{(max(nums) if nums else 0) + 1:0{width}d}"
