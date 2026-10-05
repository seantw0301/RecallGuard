from sqlalchemy.orm import Session

from backend.db.schema import AttributionResult
from backend.replay.comparator import changed_runs, condition_result


def influence_level(score: float) -> str:
    if score >= 0.67:
        return "HIGH"
    if score >= 0.34:
        return "MEDIUM"
    return "LOW"


def compute_attribution(db: Session, incident_id: str, original_action: str,
                        per_memory: dict[str, list]) -> list[AttributionResult]:
    """score = counterfactual runs that changed the action / total runs. 'Influence', not proven cause."""
    db.query(AttributionResult).filter_by(incident_id=incident_id).delete()
    rows = []
    for memory_id, runs in per_memory.items():
        cond = condition_result(runs)
        changed = changed_runs(runs, original_action)
        score = round(changed / cond.total_runs, 2) if cond.total_runs else 0.0
        rows.append(AttributionResult(
            incident_id=incident_id, memory_id=memory_id, original_action=original_action,
            counterfactual_action=cond.action, action_changed=bool(cond.action and cond.action != original_action),
            attribution_score=score, influence=influence_level(score), status=cond.stability,
            changed_runs=changed, total_runs=cond.total_runs))
    db.add_all(rows)
    db.commit()
    return sorted(rows, key=lambda r: (-r.attribution_score, r.memory_id))
