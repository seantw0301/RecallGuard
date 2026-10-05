# L9 — Agent

MVP is single-agent + deterministic services. No multi-agent fleet (explicit non-goal).

## Agent List

| Agent | Type | Role |
|---|---|---|
| Personal Agent | Nemotron-backed | Decide from request + ACTIVE memories |
| Replay Agent | Nemotron-backed | Same decision function over modified snapshot |
| Comparator | Deterministic code | Compare actions, stability, score |
| Human Reviewer | Person | Inspect, quarantine/restore/revoke |

Personal Agent and Replay Agent share one `nebius_decide` path → replay fidelity.

## Responsibility Matrix

| Duty | Personal | Replay | Comparator | Human |
|---|:-:|:-:|:-:|:-:|
| Choose option (live) | R | | | |
| Choose option (replay) | | R | | |
| Freeze snapshot | | | | |
| Compare/score | | | R | |
| Declare incident | | | A (auto rule) | R (manual) |
| Quarantine/revoke | | | | R |
| Approve verification | | | | A |

R = responsible, A = accountable. Snapshot freezing is system code on incident creation.

## Collaboration

```text
Personal Agent → decision → Incident → Snapshot
Replay Agent ←── snapshot variants ──┘
Replay Agent → runs → Comparator → attribution → Human → quarantine → Personal Agent
```

## Permission Matrix

| Actor | Read memories | Write memories | Change status | Call Nemotron | Read snapshots | Write runs |
|---|:-:|:-:|:-:|:-:|:-:|:-:|
| Personal Agent | ACTIVE only | create | ✗ | ✅ | ✗ | ✗ |
| Replay Agent | snapshot copy only | ✗ | ✗ | ✅ | ✅ | ✅ |
| Comparator | ✗ | ✗ | ✗ | ✗ | ✅ | read |
| Human | all | create | ✅ | ✗ | ✅ | ✗ |

Key rules:

- Agents never quarantine memory (human-in-the-loop remediation).
- Replay Agent reads frozen snapshot content, not live memory.
- Comparator has no model access (prevents LLM-written verdicts).
