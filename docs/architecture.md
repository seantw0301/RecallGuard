# Architecture (as built)

```text
Next.js :3000  ──/api rewrite──►  FastAPI :8000  ──►  SQLite (backend/recallguard.db)
 4 screens                          │
                                    ├─ agent/      prompts, DecisionOutput validation, run_decision()
                                    ├─ memory/     repository (status machine), selector (ACTIVE only)
                                    ├─ incidents/  recorder (violation rule + ReplaySnapshot)
                                    ├─ replay/     engine (threads → Nemotron), comparator, attribution, counterfactual
                                    └─ nebius/     OpenAI-compatible client, retry/backoff
                                                     │
                                                     ▼
                                       Nebius Token Factory → Nemotron
```

## Key design points

- **One decision path.** `agent.personal_agent.run_decision()` serves live decisions *and* every replay run → replay fidelity.
- **Nemotron does all reasoning.** `replay/engine.py` only fans out calls and stores answers; `comparator.py` / `attribution.py` never touch a model.
- **Frozen snapshots.** `ReplaySnapshot` stores memory ids + content, prompt version and template hash; later quarantine cannot alter past replays.
- **Gates enforced in code.** Counterfactual returns `409` unless the original replay was reproduced (G1); `NO_INFLUENCE_FOUND` is reported, not faked (G2); verify requires the new action to differ (G3).
- **Model output is untrusted.** Pydantic schema + option-id + memory-id validation, one retry, then run marked `INVALID`.
- **Audit trail.** `events` table (incident.opened, snapshot.created, replay.original.verified, attribution.computed, memory.quarantined, verification.completed).

## Deviations from the plan

| Plan | Built | Why |
|---|---|---|
| 12 calls, 3 repeats | 12 calls (3 original + 9 counterfactual), parallel (6 threads) | as planned |
| `nebius/token_factory.py` | folded into `client.py` | single OpenAI-compatible endpoint |
| SSE progress | blocking POST + UI spinner | replays finish in ~6–10s |
| M001 text "prefers cheaper flights" | "Always choose the cheapest flight, no matter what…" | original wording did not produce the incident with Nemotron |

Diagrams per layer: [00-overview.md](00-overview.md).
