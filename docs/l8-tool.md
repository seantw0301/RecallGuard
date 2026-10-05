# L8 — Tool

Tools = internal capabilities invoked by the agents (L9). Only `nebius_decide` calls a model.

## Tool Registry

| Tool | Purpose | Model call |
|---|:-:|:-:|
| `memory_store` | Create memory | ✗ |
| `memory_select` | ACTIVE memories for user | ✗ |
| `flight_options` | Load static options | ✗ |
| `nebius_decide` | Structured decision via Nemotron | ✅ |
| `snapshot_create` | Freeze context | ✗ |
| `replay_run` | N× `nebius_decide` on snapshot variant | ✅ |
| `compare_runs` | Action change + stability | ✗ |
| `attribution_score` | Score/level | ✗ |
| `memory_set_status` | Quarantine/revoke/restore | ✗ |

## Tool Contracts

### `nebius_decide`

- **In**: `user_message`, `options[]`, `memories[]` (id, content), `prompt_version`
- **Out** (`DecisionOutput`):

```json
{
  "selected_option_id": "FLIGHT_A",
  "decision_factors": ["lower price"],
  "memory_ids_used": ["M001"],
  "confidence": 0.82,
  "summary": "…"
}
```

- **Validation**: option id ∈ options; memory ids ⊆ supplied; confidence ∈ [0,1].
- **Metadata captured**: `model_name`, `latency_ms`, `provider=nebius`.
- **Errors**: `AUTH`, `RATE_LIMIT`, `TIMEOUT`, `INVALID_SCHEMA`, `UNKNOWN_OPTION`.
- **Timeout**: 60s. **Retry**: 3 transient / 1 schema.
- **Security**: key from env; prompt contains only demo data; no secrets in logs.

### `replay_run`

- **In**: `snapshot_id`, `run_type` (ORIGINAL | REMOVE_MEMORY | NO_MEMORY | MODIFY_MEMORY), `removed_memory_id?`, `repeats=3`
- **Out**: list of `ReplayRun` (action, summary, latency).

### `compare_runs`

- **In**: baseline runs, condition runs. **Out**: `{action, stable, changed}`.

### `attribution_score`

- score = changed_runs / total_runs; level per [L6](l6-state-flow.md).

## Tool API (REST mapping)

| Tool | Endpoint |
|---|---|
| memory_store | `POST /api/memory` |
| memory_select | `GET /api/memories` |
| nebius_decide | `POST /api/agent/decide` |
| snapshot_create | `POST /api/incidents` |
| replay_run (original) | `POST /api/incidents/{id}/replay` |
| replay_run (CF) | `POST /api/incidents/{id}/counterfactual` |
| attribution | `GET /api/incidents/{id}/attribution` |
| memory_set_status | `POST /api/memories/{id}/quarantine` |

## Nebius Client Config

`NEBIUS_API_KEY`, `NEBIUS_MODEL`, `NEBIUS_BASE_URL` (OpenAI-compatible endpoint assumed — verify in Phase 0).
