import json
from dataclasses import dataclass

from sqlalchemy.orm import Session

from backend.agent.decision_schema import DecisionOutput, DecisionValidationError, parse_decision
from backend.agent.prompts import build_messages
from backend.config import DATA_DIR
from backend.db.schema import ChatSession, Decision, DecisionRequest, next_id
from backend.memory.selector import select_active
from backend.nebius.models import LLM


def load_options() -> list[dict]:
    return json.loads((DATA_DIR / "flights.json").read_text())


@dataclass
class DecisionResult:
    output: DecisionOutput
    model_name: str
    latency_ms: int
    attempts: int


def run_decision(llm: LLM, user_message: str, options: list[dict], memories: list[dict]) -> DecisionResult:
    """Single Nemotron decision. Used by BOTH the live agent and every replay (same path = fidelity)."""
    messages = build_messages(user_message, options, memories)
    option_ids = {o["id"] for o in options}
    memory_ids = {m["id"] for m in memories}
    last: Exception | None = None
    for _ in range(2):  # one retry on schema-invalid output
        chat = llm.chat_json(messages)
        try:
            out = parse_decision(chat.text, option_ids, memory_ids)
            return DecisionResult(out, chat.model, chat.latency_ms, chat.attempts)
        except DecisionValidationError as e:
            last = e
    raise last  # type: ignore[misc]


def decide(db: Session, llm: LLM, session_id: str, message: str, kind: str = "LIVE") -> Decision:
    session = db.get(ChatSession, session_id)
    if session is None:
        raise KeyError(session_id)
    options = load_options()
    memories = select_active(db, session.user_id)
    res = run_decision(llm, message, options, memories)

    req = DecisionRequest(id=next_id(db, DecisionRequest, "R"), session_id=session_id,
                          user_message=message, options_json=options)
    db.add(req)
    db.flush()
    dec = Decision(
        id=next_id(db, Decision, "D"), request_id=req.id, kind=kind,
        selected_option_id=res.output.selected_option_id, reasoning_summary=res.output.summary,
        decision_factors_json=res.output.decision_factors,
        memory_ids_used_json=res.output.memory_ids_used, memories_json=memories,
        confidence=res.output.confidence, model_name=res.model_name, latency_ms=res.latency_ms)
    db.add(dec)
    db.commit()
    return dec
