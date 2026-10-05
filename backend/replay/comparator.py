"""Deterministic comparison. No model access: the verdict is never LLM-written."""
from collections import Counter
from dataclasses import dataclass


@dataclass
class ConditionResult:
    action: str | None  # majority action across completed runs
    stability: str  # STABLE | UNSTABLE | INCOMPLETE
    total_runs: int
    valid_runs: int
    counts: dict


def condition_result(runs) -> ConditionResult:
    valid = [r for r in runs if r.status == "COMPLETED" and r.selected_option_id]
    counts = Counter(r.selected_option_id for r in valid)
    action = counts.most_common(1)[0][0] if counts else None
    if len(valid) < len(runs) or not valid:
        stability = "INCOMPLETE"
    else:
        stability = "STABLE" if len(counts) == 1 else "UNSTABLE"
    return ConditionResult(action, stability, len(runs), len(valid), dict(counts))


def changed_runs(runs, original_action: str) -> int:
    return sum(1 for r in runs if r.status == "COMPLETED" and r.selected_option_id != original_action)
