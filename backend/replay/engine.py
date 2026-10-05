from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field

from sqlalchemy.orm import Session

from backend.agent.personal_agent import run_decision
from backend.config import settings
from backend.db.schema import ReplayRun, ReplaySnapshot
from backend.nebius.models import LLM


@dataclass(frozen=True)
class Condition:
    key: str  # e.g. "ORIGINAL", "REMOVE:M001"
    run_type: str  # ORIGINAL | REMOVE_MEMORY | NO_MEMORY | MODIFY_MEMORY
    memories: tuple  # tuple of {"id","content"} frozen dicts as (id, content) pairs
    removed_memory_id: str | None = None


@dataclass
class _Raw:
    status: str = "COMPLETED"
    action: str | None = None
    summary: str | None = None
    factors: list = field(default_factory=list)
    ids_used: list = field(default_factory=list)
    model: str | None = None
    latency_ms: int = 0
    attempts: int = 1
    error: str | None = None


def _one(llm: LLM, snap: ReplaySnapshot, memories: list[dict]) -> _Raw:
    try:
        r = run_decision(llm, snap.user_message, snap.options_json, memories)
    except Exception as e:  # noqa: BLE001 - recorded on the run, surfaced as INVALID/FAILED
        kind = "INVALID" if e.__class__.__name__ == "DecisionValidationError" else "FAILED"
        return _Raw(status=kind, error=str(e)[:500])
    o = r.output
    return _Raw("COMPLETED", o.selected_option_id, o.summary, o.decision_factors, o.memory_ids_used,
                r.model_name, r.latency_ms, r.attempts)


def run_batch(db: Session, llm: LLM, snap: ReplaySnapshot, conditions: list[Condition],
              repeats: int | None = None) -> dict[str, list[ReplayRun]]:
    """Real Nemotron inference for every (condition x repeat). Threads call the model; rows saved here."""
    repeats = repeats or settings().repeats
    jobs = [(c, i) for c in conditions for i in range(repeats)]
    with ThreadPoolExecutor(settings().concurrency) as ex:
        raws = list(ex.map(lambda j: _one(llm, snap, [{"id": a, "content": b} for a, b in j[0].memories]), jobs))
    out: dict[str, list[ReplayRun]] = {c.key: [] for c in conditions}
    for (c, i), raw in zip(jobs, raws):
        run = ReplayRun(
            snapshot_id=snap.id, run_type=c.run_type, run_index=i, removed_memory_id=c.removed_memory_id,
            selected_option_id=raw.action, reasoning_summary=raw.summary, decision_factors_json=raw.factors,
            memory_ids_used_json=raw.ids_used, status=raw.status, error=raw.error,
            model_name=raw.model, latency_ms=raw.latency_ms, attempts=raw.attempts)
        db.add(run)
        out[c.key].append(run)
    db.commit()
    return out


def snapshot_memories(snap: ReplaySnapshot) -> tuple:
    return tuple((m["id"], m["content"]) for m in snap.memories_json)
