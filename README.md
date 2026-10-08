# RecallGuard

> Counterfactual memory replay for personal AI. **Find the memory that changed the agent's mind.**

Nebius × NVIDIA Global AI Hackathon — Personal AI track · Python · FastAPI · Next.js · SQLite · Nebius Token Factory + Nemotron

## One-line pitch
When a personal AI makes a bad decision, RecallGuard has **Nemotron** replay the exact memory context, removes one memory at a time, and shows which memory changed the action — then a human quarantines it.

## Problem
Persistent memory makes AI personal, but a stale or over-weighted memory silently drives bad actions. Users can't see or test which memory did it.

## Why Personal AI
One person, many sessions, long-lived memories — the place where "why did my assistant do that?" matters most.

## What We Built
Memory store → Nemotron decision → incident + frozen snapshot → original replay (3×) → remove-one counterfactual replays (3× each) → attribution → quarantine → verified behavior change.

## Demo
```bash
scripts/install.sh       # uv + npm + Playwright
# put NEBIUS_API_KEY in .env (see .env.example)
scripts/start.sh         # http://localhost:3000
scripts/record-demo.sh   # artifacts/recallguard-demo.webm (~95 s)
```
Walkthrough: [docs/demo-script.md](docs/demo-script.md). Live result (real Nemotron, `nvidia/nemotron-3-super-120b-a12b`):

| Condition | Result | Changed? |
|---|---|---|
| All memories | Flight A (3/3) | baseline |
| Without M001 | Flight C (3/3) | **YES** → HIGH, 1.00 |
| Without M002 | Flight A (3/3) | NO |
| Without M003 | Flight A (3/3) | NO |
| After quarantining M001 | Flight C | behavior changed |

## Architecture
See [docs/architecture.md](docs/architecture.md) and the 12-layer analysis in [docs/00-overview.md](docs/00-overview.md).

## How Counterfactual Replay Works
Snapshot freezes request, options, memory ids + content, model, prompt version. For each memory: replay without it ×3 with Nemotron; compare the majority action to the original.

## Nemotron Integration
`backend/nebius/client.py` (OpenAI-compatible Token Factory). **Every** decision and replay call goes through `agent.personal_agent.run_decision()` → Nemotron. Code never decides replay outcomes; it only compares.

## Replay Stability
3 runs/condition. Mixed answers → `UNSTABLE`. Original replay must reproduce the action (Gate 1) or attribution is blocked (`409`).

## Memory Attribution
`score = changed runs / total runs` → HIGH ≥ 0.67, MEDIUM ≥ 0.34, else LOW. Reported as *counterfactual influence*, not proven causality. `memory_ids_used` is model-reported, not proof.

## Quarantine
`POST /api/memories/{id}/quarantine` → status `QUARANTINED`; selector sends only ACTIVE memories. Restore / revoke supported.

## Setup
Requires `uv`, Node ≥ 20, a Nebius Token Factory key. `scripts/install.sh`, then `scripts/start.sh` / `scripts/stop.sh`.

## Environment Variables
```text
NEBIUS_API_KEY=        # secret, never committed
NEBIUS_MODEL=nvidia/nemotron-3-super-120b-a12b
NEBIUS_BASE_URL=https://api.tokenfactory.nebius.com/v1
```

## Tests
```bash
scripts/test.sh                 # 18 offline tests (fake transport — no model claims)
RUN_LIVE=1 scripts/test.sh      # + full loop against real Nemotron (gates 1–3)
```
Playwright demo (`demo/`) doubles as the e2e test against live Nemotron.

## Demo Recording
30 s opening + product demo, neural voice (Kokoro, local) → `artifacts/recallguard-final.mp4` (≈2:16, git-ignored). See [docs/demo-voice.md](docs/demo-voice.md).

## Product Feedback
[docs/product-feedback.md](docs/product-feedback.md)

## Friction Log
[docs/friction-log.md](docs/friction-log.md)

## Limitations
- Single scenario, single user, three memories; seed wording tuned to Nemotron (documented).
- Single-memory removal only (joint effects missed).
- Temperature 0 is not fully deterministic → repeat-and-vote, not a guarantee.
- Incident detection is a demo heuristic (overnight layover vs. avoid-memory) plus manual report.
- Replays block the HTTP call (~10 s); no SSE; crash-resume not implemented.
- Memories are sent to Nebius for inference; demo uses synthetic data only.

## What Was Built for This Hackathon
Everything in this repo, created for the hackathon; plan in [docs/source-plan.md](docs/source-plan.md).

## Future Work
MODIFY_MEMORY runs, pairwise removal, factor-level MEDIUM influence, more scenarios, PostgreSQL, SSE progress.

## Live
https://recallguard.jxdtw.com — deployment: [docs/deploy.md](docs/deploy.md)

## Docs
[Overview](docs/00-overview.md) · L1 [Business](docs/l1-business.md) · L2 [Product](docs/l2-product.md) · L3 [AI](docs/l3-ai-strategy.md) · L4 [Workflow](docs/l4-workflow.md) · L5 [Data](docs/l5-data-flow.md) · L6 [State](docs/l6-state-flow.md) · L7 [Memory](docs/l7-memory.md) · L8 [Tool](docs/l8-tool.md) · L9 [Agent](docs/l9-agent.md) · L10 [Service](docs/l10-service.md) · L11 [Event](docs/l11-event.md) · L12 [Infra](docs/l12-infrastructure.md) · [Devpost](docs/devpost.md)

MIT License
