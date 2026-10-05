# L1 — Business

## Business Goal

- Win/contend in Nebius × NVIDIA hackathon, Personal AI track.
- Prove: personal AI memory can be audited — "which memory changed the action?"

## Problem

- Persistent memory makes AI personal, but a stale/wrong/over-weighted memory silently causes bad actions.
- Users cannot see or test which memory drove a decision.

## Stakeholders

| Stakeholder | Interest |
|---|---|
| End user (persistent AI assistant user) | Understand and fix bad decisions |
| Hackathon judges | Nemotron central, working demo, track fit |
| Nebius / NVIDIA | Token Factory + Nemotron showcase, product feedback |
| Dev team | Deliver demo + repo + Devpost on deadline |

## Persona

- Uses a persistent AI assistant across many sessions.
- Wants to know *why* the assistant made a bad choice, and to correct it.

## Value Proposition

> Personal AI should not only remember. It should show which memory changed its behavior.

- Reproduce the incident (replay).
- Isolate influence (remove one memory, replay).
- Fix it (human quarantine) and verify (future decision changes).

## KPI (hackathon-scale)

| KPI | Target |
|---|---|
| Nemotron used for replay reasoning | 100% of replay runs |
| Original replay reproducibility | 3/3 |
| M001 removal action-change rate | 3/3 runs |
| M002/M003 removal change rate | 0/3 |
| Post-quarantine action ≠ original | Yes |
| Demo length | ≤ 3:00, auto-recorded |
| Deliverables | Public repo, MIT license, README, Devpost, feedback, friction log |

## MVP Goal

One incident (Tokyo flight), full loop: memory → incident → replay → counterfactual → attribution → quarantine → changed behavior.

## Non-Goals

- Enterprise observability, fleet management, multi-agent monitoring.
- Real bookings / integrations.
