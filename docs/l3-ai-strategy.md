# L3 — AI Strategy

## Principle

> Nemotron performs the decision and every replay. Code never decides replay outcomes.

## AI Capability Matrix

| Capability | LLM (Nemotron) | Rules/Code |
|---|:-:|:-:|
| Original agent decision | ✅ | |
| Original replay | ✅ | |
| Counterfactual replay | ✅ | |
| Option validation (id exists) | | ✅ |
| Action-change comparison | | ✅ |
| Attribution score | | ✅ |
| Stability flag | | ✅ |
| Memory selection (status filter) | | ✅ |
| Incident trigger (constraint violated) | | ✅ |
| Quarantine | | ✅ (human-initiated) |

## AI Decision Points

| # | Point | Input | Output |
|---|---|---|---|
| D1 | Agent decision | request + options + ACTIVE memories | DecisionOutput |
| D2 | Original replay | snapshot (same everything) | DecisionOutput ×3 |
| D3 | Counterfactual replay | snapshot − 1 memory | DecisionOutput ×3 per memory |
| D4 (optional) | Post-quarantine decision | request + options + ACTIVE memories | DecisionOutput |

## LLM Scope

- Select exactly one option from supplied options using supplied memories.
- Return JSON only: `selected_option_id`, `decision_factors`, `memory_ids_used`, `confidence`, `summary`.
- No hidden chain-of-thought stored; only `summary` + factors.

## Non-LLM Scope

- Compare actions, compute score, mark UNSTABLE, filter memories, persist snapshots.
- LLM must NOT write the attribution verdict (avoids "Python decides, Nemotron narrates" inversion).

## Determinism Controls

- Same model, `prompt_version`, `system_prompt_hash`, options order, memory order.
- temperature = 0 (and seed if API supports).
- 3 runs per condition; majority action = condition result; disagreement → UNSTABLE.

## Evidence Language

- Use: "counterfactual contribution", "decision influence", "material influence".
- Avoid: "proven cause".
- `memory_ids_used` = model-reported evidence, not proof.

## Failure Handling

| Failure | Behavior |
|---|---|
| Invalid JSON / schema | Retry once, then mark run INVALID |
| Unknown option / memory id | Reject run |
| Original replay ≠ original action | `REPLAY_UNSTABLE`, stop attribution (Gate 1) |
| No memory changes action | Report; rewrite scenario (Gate 2); never fake |
