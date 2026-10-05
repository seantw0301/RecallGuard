from types import SimpleNamespace as NS

from backend.replay.attribution import influence_level
from backend.replay.comparator import changed_runs, condition_result


def runs(*actions, status="COMPLETED"):
    return [NS(selected_option_id=a, status=status) for a in actions]


def test_attribution_score_levels():
    assert influence_level(1.0) == "HIGH" and influence_level(0.67) == "HIGH"
    assert influence_level(0.34) == "MEDIUM" and influence_level(0.33) == "LOW" and influence_level(0) == "LOW"


def test_changed_fraction_and_stability():
    r = runs("B", "B", "A")
    assert changed_runs(r, "A") == 2
    c = condition_result(r)
    assert c.stability == "UNSTABLE" and c.action == "B"
    assert condition_result(runs("B", "B", "B")).stability == "STABLE"
    assert condition_result(runs("B", None, "B", status="FAILED")).stability == "INCOMPLETE"
