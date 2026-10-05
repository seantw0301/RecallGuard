import json

from pydantic import BaseModel, Field, ValidationError


class DecisionValidationError(Exception):
    pass


class DecisionOutput(BaseModel):
    selected_option_id: str
    decision_factors: list[str]
    memory_ids_used: list[str]  # model-reported evidence, not proof
    confidence: float = Field(ge=0, le=1)
    summary: str


def parse_decision(text: str, option_ids: set[str], memory_ids: set[str]) -> DecisionOutput:
    """Never trust raw model output: extract JSON, validate schema, option and memory ids."""
    try:
        raw = json.loads(text[text.index("{"): text.rindex("}") + 1])
        out = DecisionOutput.model_validate(raw)
    except (ValueError, ValidationError) as e:
        raise DecisionValidationError(f"invalid JSON/schema: {e}") from e
    if out.selected_option_id not in option_ids:
        raise DecisionValidationError(f"unknown option {out.selected_option_id!r}")
    unknown = set(out.memory_ids_used) - memory_ids
    if unknown:
        raise DecisionValidationError(f"unknown memory ids {sorted(unknown)}")
    return out
