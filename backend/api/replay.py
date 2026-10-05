from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.api import serializers as ser
from backend.api.incidents import get_incident, get_snapshot
from backend.db.database import get_db
from backend.db.schema import AttributionResult, Decision, ReplayRun
from backend.nebius.client import get_llm
from backend.replay.comparator import condition_result
from backend.replay.counterfactual import ReplayStateError, run_counterfactual, run_original

from backend.config import settings

N = settings().repeats
router = APIRouter(prefix="/api")


def _stability(runs) -> dict:
    r = condition_result(runs)
    return {"action": r.action, "stability": r.stability, "counts": r.counts}


@router.post("/incidents/{incident_id}/replay")
def replay_original(incident_id: str, db: Session = Depends(get_db), llm=Depends(get_llm)):
    inc = get_incident(db, incident_id)
    runs = run_original(db, llm, inc, get_snapshot(db, inc.id), db.get(Decision, inc.decision_id))
    return {"incident_status": inc.status, "reproduced": inc.original_reproduced,
            "original_action": db.get(Decision, inc.decision_id).selected_option_id,
            **_stability(runs), "runs": [ser.run(r) for r in runs]}


@router.post("/incidents/{incident_id}/counterfactual")
def counterfactual(incident_id: str, include_no_memory: bool = False,
                   db: Session = Depends(get_db), llm=Depends(get_llm)):
    inc = get_incident(db, incident_id)
    try:
        rows = run_counterfactual(db, llm, inc, get_snapshot(db, inc.id),
                                  db.get(Decision, inc.decision_id), include_no_memory)
    except ReplayStateError as e:
        raise HTTPException(409, str(e))
    return {"incident_status": inc.status, "attribution": [ser.attribution(r) for r in rows]}


@router.get("/incidents/{incident_id}/attribution")
def attribution(incident_id: str, db: Session = Depends(get_db)):
    inc = get_incident(db, incident_id)
    snap = get_snapshot(db, inc.id)
    rows = db.scalars(select(AttributionResult).where(AttributionResult.incident_id == inc.id)
                      .order_by(AttributionResult.attribution_score.desc(), AttributionResult.memory_id)).all()
    runs = db.scalars(select(ReplayRun).where(ReplayRun.snapshot_id == snap.id).order_by(ReplayRun.id)).all()
    orig = [r for r in runs if r.run_type == "ORIGINAL"]
    # latest batch per condition (repeat clicks must not mix old and new runs)
    latest: dict = {}
    for r in runs:
        if r.run_type != "ORIGINAL":
            latest.setdefault(r.removed_memory_id or r.run_type, []).append(r)
    n = len(orig[-N:]) if orig else 0
    return {"incident_status": inc.status, "ranked": [ser.attribution(a) for a in rows],
            "original_runs": [ser.run(r) for r in orig[-N:]],
            "counterfactual_runs": {k: [ser.run(r) for r in v[-N:]] for k, v in latest.items()},
            "model_name": snap.model_name, "n_repeats": n}
