from sqlalchemy.orm import Session

from backend.db.schema import Decision, Incident, ReplaySnapshot
from backend.events import publish
from backend.nebius.models import LLM
from backend.replay.attribution import compute_attribution
from backend.replay.comparator import condition_result
from backend.replay.engine import Condition, run_batch, snapshot_memories


class ReplayStateError(Exception):
    pass


def run_original(db: Session, llm: LLM, inc: Incident, snap: ReplaySnapshot, dec: Decision) -> list:
    """Gate 1: replay with the exact snapshot; must reproduce the original action."""
    inc.status = "REPLAYING"
    db.commit()
    mems = snapshot_memories(snap)
    runs = run_batch(db, llm, snap, [Condition("ORIGINAL", "ORIGINAL", mems)])["ORIGINAL"]
    res = condition_result(runs)
    inc.original_stability = res.stability
    inc.original_reproduced = res.stability == "STABLE" and res.action == dec.selected_option_id
    inc.status = "REPLAYING" if inc.original_reproduced else "REPLAY_UNSTABLE"
    db.commit()
    publish(db, "replay.original.verified" if inc.original_reproduced else "replay.unstable", inc.id,
            {"stability": res.stability, "action": res.action})
    return runs


def run_counterfactual(db: Session, llm: LLM, inc: Incident, snap: ReplaySnapshot, dec: Decision,
                       include_no_memory: bool = False) -> list:
    if not inc.original_reproduced:
        raise ReplayStateError("original replay not verified (Gate 1)")
    mems = snapshot_memories(snap)
    conds = [Condition(f"REMOVE:{mid}", "REMOVE_MEMORY", tuple(m for m in mems if m[0] != mid), mid)
             for mid, _ in mems]
    if include_no_memory:
        conds.append(Condition("NO_MEMORY", "NO_MEMORY", ()))
    batch = run_batch(db, llm, snap, conds)
    per_memory = {c.removed_memory_id: batch[c.key] for c in conds if c.run_type == "REMOVE_MEMORY"}
    rows = compute_attribution(db, inc.id, dec.selected_option_id, per_memory)
    if any(r.influence == "HIGH" for r in rows):
        inc.status = "REMEDIATION_PENDING"
    elif any(r.changed_runs for r in rows):
        inc.status = "ANALYZED"
    else:
        inc.status = "NO_INFLUENCE_FOUND"  # Gate 2: rewrite scenario, never fake attribution
    db.commit()
    publish(db, "attribution.computed", inc.id, {"status": inc.status})
    return rows
