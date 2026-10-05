from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.agent.decision_schema import DecisionValidationError
from backend.agent.personal_agent import decide, load_options
from backend.api import serializers as ser
from backend.db.database import get_db
from backend.events import publish
from backend.incidents.recorder import detect_violation
from backend.nebius.client import get_llm
from backend.nebius.models import NebiusError

router = APIRouter(prefix="/api")


class DecideIn(BaseModel):
    session_id: str
    message: str


@router.get("/flights")
def flights():
    return load_options()


@router.post("/agent/decide")
def agent_decide(body: DecideIn, db: Session = Depends(get_db), llm=Depends(get_llm)):
    try:
        d = decide(db, llm, body.session_id, body.message)
    except KeyError:
        raise HTTPException(404, "session not found")
    except (NebiusError, DecisionValidationError) as e:
        raise HTTPException(502, str(e))
    options = load_options()
    publish(db, "decision.made", None, {"decision_id": d.id, "selected": d.selected_option_id})
    return ser.decision(d, options, detect_violation(d, options))
