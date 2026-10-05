# L2 — Product

## Product Modules

| Module | Purpose |
|---|---|
| Personal AI | Chat, store memories, make decisions |
| Decision | Show request, options, selected action, memories used |
| Replay Lab | Original + counterfactual replays, stability, latency |
| Memory Review | Influence ranking, quarantine/revoke |
| Demo Control | Reset demo seed |

## User Journey

1. Session 1: tell AI preferences → M001/M002/M003 stored.
2. Session 2: "Book me a flight to Tokyo next Friday." → AI picks Flight A (overnight layover).
3. User clicks **Report Incident** (or auto-flagged).
4. Replay Lab: original replay → Flight A (reproduced).
5. Counterfactual: without M001 → not A; without M002/M003 → A.
6. Memory Review: M001 = HIGH influence (1.00) → **Quarantine**.
7. Re-run same request → Flight B/C (not A).

## Feature List (MVP)

- F1 Persistent memory CRUD (preference type).
- F2 Static flight dataset (A/B/C).
- F3 Nemotron decision (structured JSON, validated).
- F4 Incident + ReplaySnapshot.
- F5 Original replay (3 runs) + stability flag.
- F6 Single-memory removal replay (3 runs each).
- F7 Attribution score + HIGH/MEDIUM/LOW.
- F8 Quarantine / revoke; selector excludes them.
- F9 4-screen UI; model name, latency, stability visible.
- F10 Demo reset; Playwright auto-recording.

## Screens

1. Personal AI — chat, memories, session.
2. Decision — request, flights, selection, Report Incident.
3. Replay Lab — table: condition / result / changed? (+ model, latency, stability).
4. Memory Review — influence, score, Quarantine.

## Roadmap

| Phase | Deliverable |
|---|---|
| 0 | Nebius+Nemotron smoke test (Gate 0) |
| 1–3 | DB, memories, flights, decision API |
| 4–8 | Snapshot, replay, counterfactual, attribution, quarantine |
| 9–11 | Frontend, tests, Playwright demo |
| 12 | README, Devpost, product feedback, friction log |
| Post | MODIFY_MEMORY, pairwise removal, more scenarios |

## Product Scope

- **In**: single scenario, single user, single incident, 3 memories.
- **Out**: see [00-overview.md](00-overview.md#out-of-scope-until-core-works).
