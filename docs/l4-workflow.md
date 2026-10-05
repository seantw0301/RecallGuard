# L4 — Workflow

## Business Process (main flow)

```mermaid
flowchart TD
  A[Session 1: store memories M001-M003] --> B[Session 2: user request]
  B --> C[Select ACTIVE memories]
  C --> D[Nemotron decision]
  D --> E{Violates active constraint?}
  E -- yes --> F[Incident created]
  E -- no --> Z[Done]
  B2[User clicks Report Incident] --> F
  F --> G[Create ReplaySnapshot]
  G --> H[Original replay x3 - Nemotron]
  H --> I{Reproduced 3/3?}
  I -- no --> U[REPLAY_UNSTABLE - stop]
  I -- yes --> J[Counterfactual: remove each memory x3 - Nemotron]
  J --> K[Compare + attribution score]
  K --> L{Any action change?}
  L -- no --> R[Gate 2: rewrite scenario]
  L -- yes --> M[Memory Review: rank influence]
  M --> N[Human: Quarantine]
  N --> O[Re-run request - memory excluded]
  O --> P[Changed action shown]
```

## Steps

| # | Step | Actor |
|---|---|---|
| 1 | Store memory | User/Personal AI |
| 2 | Submit decision request | User |
| 3 | Select ACTIVE memories | System |
| 4 | Decide | Nemotron |
| 5 | Detect / report incident | System / User |
| 6 | Snapshot context | System |
| 7 | Original replay ×3 | Nemotron |
| 8 | Remove-one replay ×3 each | Nemotron |
| 9 | Compare, score, stability | System |
| 10 | Review + quarantine | User |
| 11 | Verify future decision | Nemotron |

## Exception Flow

| Exception | Handling |
|---|---|
| Nebius unreachable / 401 | Gate 0 stop; show error, log friction |
| Rate limit / 429 | Backoff retry (max 3), log friction |
| Invalid model JSON | Retry once → INVALID run |
| Replay unstable | Stop attribution, show `REPLAY_UNSTABLE` |
| No action change | Report Gate 2 failure |
| Quarantine of non-ACTIVE memory | 409 |

## Parallel Tasks

- Counterfactual conditions (3 memories) can run concurrently (asyncio, bounded concurrency e.g. 4).
- 3 repeats per condition can run concurrently.
- Total MVP calls: (1 original + 3 CF) × 3 = **12** Nemotron calls per incident.
