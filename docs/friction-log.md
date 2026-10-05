# Friction log (real observations only)

| Task | Steps | Expected | Actual | Severity | Workaround | Suggestion |
|---|---|---|---|---|---|---|
| Find base URL | Used `https://api.tokenfactory.nebius.com/v1` | Documented endpoint works | Worked; `GET /models` listed 4 Nemotron models | Low | — | Surface base URL + model IDs in quickstart |
| Demo scenario | All 3 memories, source wording, temperature 0 | Original plan picks Flight A | Nemotron-3-Super picked Flight C (honours M002) | High (demo) | Reworded M001 stronger / M002 weaker; re-tested 6× per condition | — |
| Determinism | Same prompt, temperature 0, 6 repeats | Identical output | Old seed: one of 6 runs differed (`AAAAAC`); one live run failed Gate 1 | Medium | 3 runs/condition + UNSTABLE flag; seed tuned to 6/6 stable | Document determinism guarantees / seed support |
| Reasoning headroom | `max_tokens` small | JSON returned | Reasoning model can spend tokens before JSON; used 2000 | Low | `max_tokens=2000` | Document reasoning-token budget |
| JSON mode | `response_format: json_object` | Valid JSON | Worked; one rare response missed `selected_option_id` (caught by schema validation → retry) | Low | Pydantic + 1 retry | — |
| Rate limits | 12 calls in parallel (6 threads) | Possible 429 | None observed | None | Backoff retry implemented | — |
