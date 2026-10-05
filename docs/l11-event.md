# L11 — Event

MVP: in-process synchronous event bus (domain events recorded to an `events` audit log). No broker.

## Event Catalog

| Event | Publisher | Subscribers | Sync/Async |
|---|---|---|---|
| `memory.created` | Memory | Audit | sync |
| `decision.made` | Agent | Incident detector, Audit | sync |
| `incident.opened` | Incident | Snapshotter, Audit | sync |
| `snapshot.created` | Incident | Replay | sync |
| `replay.run.completed` | Replay | Comparator, Audit | async (bounded) |
| `replay.original.verified` | Replay | Replay (starts CF) | sync |
| `replay.unstable` | Replay | Incident state, UI | sync |
| `counterfactual.completed` | Replay | Attribution | async |
| `attribution.computed` | Attribution | UI, Incident state | sync |
| `memory.quarantined` | Memory | Selector cache invalidation (none in MVP), Audit | sync |
| `verification.completed` | Agent | Incident state → RESOLVED | sync |

## Publisher / Subscriber

- Publishers emit only after DB commit.
- Subscribers idempotent (keyed by `snapshot_id + run key`).

## Event Contract

```json
{
  "event_id": "uuid",
  "type": "replay.run.completed",
  "occurred_at": "ISO-8601",
  "incident_id": "I001",
  "payload": {
    "run_id": "…",
    "run_type": "REMOVE_MEMORY",
    "removed_memory_id": "M001",
    "selected_option_id": "FLIGHT_B",
    "model_name": "…",
    "latency_ms": 1234
  },
  "schema_version": 1
}
```

- Payloads contain IDs + decision data; never API keys; memory content only via snapshot reference.

## UI Delivery

- Replay progress: SSE `GET /api/incidents/{id}/events` (optional; polling fallback).
- Future: Redis/NATS if services split.
