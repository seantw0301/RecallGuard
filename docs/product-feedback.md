# Product feedback — Nebius Token Factory + Nemotron

Measured on `nvidia/nemotron-3-super-120b-a12b`, 2026-10-06.

| Area | Observation |
|---|---|
| Onboarding | Key + OpenAI-compatible base URL worked first try; `/models` lists Nemotron variants (Nano 30B, Super 120B, Ultra 550B, 3.5 Lightning). |
| Latency | ≈4–5 s per structured decision; 9 parallel counterfactual calls finish in ≈6–10 s total. |
| Structured output | `response_format: json_object` works; rare schema slips → validate client-side and retry once. |
| Rate limits | No 429 at 6 concurrent requests. |
| Model quality | Follows memory instructions closely; wording strength of a memory sharply moves the decision — exactly what counterfactual replay exposes. |
| Determinism | Temperature 0 is not fully deterministic across repeats (1/6 flip on a borderline seed). Replay tools need repeat-and-vote. |
| Docs wish | Document reasoning-token budgeting, determinism/seed support, and error body formats. |
| Error handling | 401 returned for bad key (client treats AUTH as non-retryable). |

See [friction-log.md](friction-log.md).
