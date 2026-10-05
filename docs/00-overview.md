# RecallGuard — Overview & Analysis

> Find the memory that changed the agent's mind.

Source: [source-plan.md](source-plan.md) (original hackathon plan, unmodified).
Target: Nebius × NVIDIA Global AI Hackathon — Personal AI track.

## 12-Layer Index

| L | Doc | Question |
|---|-----|----------|
| 1 | [l1-business.md](l1-business.md) | Why / who / KPI |
| 2 | [l2-product.md](l2-product.md) | What features / scope |
| 3 | [l3-ai-strategy.md](l3-ai-strategy.md) | Where LLM vs rules |
| 4 | [l4-workflow.md](l4-workflow.md) | Step flow |
| 5 | [l5-data-flow.md](l5-data-flow.md) | Data paths |
| 6 | [l6-state-flow.md](l6-state-flow.md) | State machines |
| 7 | [l7-memory.md](l7-memory.md) | Memory strategy |
| 8 | [l8-tool.md](l8-tool.md) | Tool contracts |
| 9 | [l9-agent.md](l9-agent.md) | Agents / permissions |
| 10 | [l10-service.md](l10-service.md) | Services / API |
| 11 | [l11-event.md](l11-event.md) | Events |
| 12 | [l12-infrastructure.md](l12-infrastructure.md) | Tech / deploy / security |

## One-paragraph essence

- Personal AI stores persistent memories → later makes a bad action.
- Snapshot exact context → Nemotron replays original.
- Remove one memory at a time → Nemotron replays again (3× each).
- Action change = counterfactual influence → human quarantines memory.
- Future decision changes. Loop closed.

## Analysis findings (gaps & risks in the source plan)

| # | Finding | Impact | Resolution |
|---|---------|--------|------------|
| A1 | Scenario depends on model overweighting M001 (cheap) over M002 (avoid overnight). A capable model may pick Flight C even with all memories. | Gate 2 fails | Tune seed wording / prompt; never hard-code. Phase 6 tuning step. |
| A2 | Expected post-removal result "Flight B" is not guaranteed; Flight C ($355, 1 stop, no overnight) is also valid. | Brittle demo assertions | Assert `action != FLIGHT_A` and chosen option has no overnight layover — not exact B. |
| A3 | "Incident" trigger is undefined in source. | Ambiguous detection | Define `CONSTRAINT_VIOLATION`: selected option violates an ACTIVE memory constraint (M002). Manual "Report Incident" also allowed. |
| A4 | `memory_ids_used` is self-reported by model. | Over-claiming | Show as "model-reported"; attribution relies on counterfactual change only. |
| A5 | Single-removal misses joint effects (M001+M003). | Under-attribution | Declared limitation; pairwise removal = future work. |
| A6 | LLM nondeterminism. | Flaky attribution | temperature=0, fixed seed if supported, 3 runs/condition, UNSTABLE flag, Gate 1. |
| A7 | Source stack (Python/Next.js/SQLite) differs from global default. | Rule conflict | User confirmed Python, FastAPI, Next.js, SQLite (see L12). |
| A8 | Source repo name `recallguard`; user requested `RecallGuard`. | Naming | GitHub repo = `RecallGuard`; Python pkg stays lowercase. |
| A9 | Nebius model ID / base URL unknown. | Gate 0 blocker | Env vars; smoke test first (Phase 0). |

## Gates (carried from source)

- **G0** Nemotron callable via Nebius Token Factory, else stop.
- **G1** Original replay reproduces action (3/3), else `REPLAY_UNSTABLE`.
- **G2** ≥1 memory removal changes action, else rewrite scenario (never fake).
- **G3** Quarantine changes future memory selection.

## Phases

0 smoke → 1 DB+memories → 2 flights → 3 decision API → 4 snapshot → 5 original replay → 6 counterfactual → 7 attribution → 8 quarantine → 9 frontend → 10 tests → 11 Playwright demo → 12 README/Devpost/feedback.

## Out of scope (until core works)

Multi-agent fleet, blast radius, restore checkpoint, causal graph, SRE dashboard, calendar/email, real booking, vector DB, knowledge graph, local model fallback, multiple incidents.
