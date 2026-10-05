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

## Hackathon feedback form — draft answers

- **Output quality (1–10):** 8 — follows memory instructions closely, valid JSON almost always (rare schema slip caught by validation).
- **Approach:** out of the box, prompt-engineered only (one shared prompt template; memory wording tuned against the live model). No fine-tuning.
- **Vs other models:** not benchmarked head-to-head here; Nemotron-3-Super was more instruction-faithful than needed for the original scenario (it honoured a soft "avoid overnight" memory), which forced stronger seed wording.
- **Most valuable Nebius capabilities:** OpenAI-compatible Token Factory endpoint (zero-friction client), `/models` discovery of Nemotron variants, low-latency parallel inference (9 concurrent calls in ~6–10 s, no 429s), JSON mode.
- **Recommend (1–10):** 8. **Experience vs other envs (1–10):** 8 — key + base URL working in minutes.
- **Wanted improvements:** documented determinism/seed support, reasoning-token budgeting guidance, per-request token/latency metadata, logprobs for decision confidence.
- **Hope from Nemotron team:** deterministic/seeded decoding, native structured-output (JSON schema) guarantees, logprobs, smaller fast model with the same instruction fidelity.
- **Tavily:** not used.
- **Builders & Brews IRL city:** not answered — needs your input.
