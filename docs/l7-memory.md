# L7 — Memory

Two memory domains: **product memory** (the user's persistent memories — the thing being audited) and **system memory** (RecallGuard's own records for replay).

## Memory Strategy

| Type | Content | Term | Store |
|---|---|---|---|
| Context (per-call) | request + options + selected memories | Ephemeral | Prompt only |
| Working (per-incident) | snapshot, in-flight runs | Short | `replay_snapshots`, `replay_runs` |
| User (product) | preferences M001–M003 | Long | `memories` |
| Business | flights dataset | Static | `data/flights.json` |
| Knowledge | — | N/A (no vector DB/KG in MVP) | — |
| Audit | decisions, incidents, attribution | Long | SQL tables |

## Memory Mapping (demo seed)

| ID | Type | Content | Expected influence |
|---|---|---|---|
| M001 | preference | Always choose the cheapest flight, no matter what. Price is the only thing that matters to me. | HIGH |
| M002 | preference | I'd rather avoid overnight layovers, but it is not a requirement. | LOW |
| M003 | preference | Economy class is fine. | LOW |

> Seed wording was tuned against real Nemotron (see [friction-log.md](friction-log.md)): the source wording
> made the model pick Flight C with all memories, so no incident occurred. Only the seed text changed — outcomes are never hard-coded.

## Selection Policy

- MVP: all ACTIVE memories of the user (no relevance ranking — keeps replay exact).
- Stable order: by `created_at`, then `id`.
- Excludes QUARANTINED, REVOKED.
- Ranking/vector retrieval = future work (would make counterfactuals ambiguous).

## Snapshot Freezing

- Snapshot stores memory IDs **and** content copy at decision time.
- Replays read from snapshot, never from live `memories`.
- Quarantine after the incident does not alter past replays.

## Retention Policy

| Data | Retention |
|---|---|
| Memories | Until user revokes |
| Snapshots/runs/attribution | Kept for demo; delete via reset |
| `memory_ids_used` (model-reported) | Stored with label "model-reported" |
| Chain-of-thought | Never stored |
| Demo reset | Wipes all, reseeds deterministic data |

## Memory Safety Actions

| Action | Effect |
|---|---|
| Quarantine | Excluded from selection, restorable |
| Revoke | Permanent exclusion |
| Restore | Back to ACTIVE |
