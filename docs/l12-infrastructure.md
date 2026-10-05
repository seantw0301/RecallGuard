# L12 — Infrastructure

## Tech Selection

| Area | Choice | Note |
|---|---|---|
| Frontend | Next.js + TypeScript + Tailwind | Per source plan |
| Backend | Python 3.12, FastAPI, Pydantic, SQLAlchemy | Per source plan |
| DB | SQLite (MVP) → PostgreSQL later | Per source plan |
| Model runtime | Nebius Token Factory + Nemotron | **Mandatory** (competition) |
| Tests | pytest, Playwright | |
| Demo video | Playwright recording + FFmpeg | |
| License | MIT | Open-source requirement |

### Rule exception (explicit)

- Global default stack = PHP / Flutter / MySQL.
- This project follows the **source plan's explicit stack** (user-provided spec) because Nebius/Nemotron hackathon tooling is Python/TS-oriented.
- Override rule: explicit user tech > default.

## Infrastructure Diagram

```text
Dev machine (macOS)
 ├─ Next.js  :3000
 ├─ FastAPI  :8000 ── SQLite (backend/recallguard.db)
 └─ HTTPS ──► Nebius Token Factory ──► Nemotron
```

## Deployment

| Env | Setup |
|---|---|
| Local demo | `scripts/start.sh` |
| Hackathon submission | Public repo + recorded video; live deploy optional |
| Optional hosting | Single VM / container; HTTPS reverse proxy |

## DevOps

| Item | Plan |
|---|---|
| Repo | github.com/seantw0301/RecallGuard (public) |
| Branching | `main` only (hackathon) |
| CI (optional) | GitHub Actions: lint + pytest with mocked transport (Nemotron integration tests gated by secret) |
| Scripts | `install.sh`, `start.sh`, `stop.sh`, `test.sh`, `seed-demo.sh`, `record-demo.sh`, `nebius-smoke-test.py` |
| Docs | `docs/` + README entry |

## Security

| Risk | Control |
|---|---|
| API key leak | `.env` git-ignored; `.env.example` placeholders; secret scan before push |
| PII | Synthetic demo data only; README privacy note |
| Prompt injection via memory content | Memory text delimited in prompt; output schema-validated; unknown ids rejected |
| Model output trust | Pydantic validation; never executed |
| CORS | Restrict to frontend origin |
| Logs | No keys, no raw chain-of-thought |

## Observability (minimal)

- Per run: `model_name`, `latency_ms`, attempt count, status.
- Shown in UI Replay Lab; used for Nebius product feedback.

## Testing Strategy

- Unit: selector, comparator, attribution, state transitions (no network).
- Integration (real Nemotron, gated): original replay reproducibility; M001 removal changes action; M002/M003 don't.
- E2E: Playwright full demo.
- Required test list per [source plan §24](source-plan.md).

## Disaster Recovery

| Scenario | Recovery |
|---|---|
| DB corrupt | `POST /api/demo/reset` / `scripts/seed-demo.sh` |
| Nebius outage on demo day | Pre-recorded video (`artifacts/recallguard-demo.webm`); **no** alternative-model substitution claimed as compliant (Gate 0) |
| Lost repo | GitHub remote |

## Repo Layout

Per [source plan §8](source-plan.md), lowercase Python/TS packages under `backend/`, `frontend/`, plus `data/`, `demo/`, `docs/`, `scripts/`.
