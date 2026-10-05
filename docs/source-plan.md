# RecallGuard — Counterfactual Memory Replay for Personal AI
## Repo & DEMO Implementation Plan

> Target: Nebius × NVIDIA Global AI Hackathon — Personal AI Track  
> Project type: Pure Software / Web Application  
> Development environment: Claude IDE / AI Coding Agent  
> Core idea: When a personal AI makes a bad decision, replay the exact memory context with Nemotron, remove or alter individual memories, and observe whether the agent's action changes.

---

# 1. Project Goal

Build a working software demo that proves:

1. A Personal AI stores persistent memories across sessions.
2. A later action is influenced by those memories.
3. When an incident occurs, the system captures the exact memory context used.
4. Nemotron performs the original replay.
5. Nemotron performs counterfactual replays with individual memories removed or changed.
6. The system compares outputs and estimates which memory materially changed the action.
7. A suspicious memory can be quarantined or marked for human review.
8. A future replay without that memory produces a different, safer decision.

Core product statement:

> Personal AI should not only remember. It should be able to explain which memory changed its behavior.

Core technical principle:

> Nemotron performs the counterfactual replay itself — not just the explanation.

---

# 2. Product Name

Recommended repository name:

```text
recallguard
```

Recommended product title:

# RecallGuard

Subtitle:

> Counterfactual memory replay for personal AI.

---

# 3. Competition Fit

This project targets the Personal AI track.

The project must remain a Personal AI memory-safety product, not an enterprise observability dashboard.

Avoid turning it into:

```text
multi-agent monitoring
fleet management
general LLM observability
enterprise incident response
```

The user persona is:

> A person who uses a persistent AI assistant over many sessions and wants to understand why the assistant made a bad decision.

---

# 4. Core Demo Story

Use exactly one incident.

Do not build many scenarios before the first demo works.

## Session 1 — Memory Formation

User tells the assistant:

```text
I usually prefer cheaper flights.
```

Stored:

```text
M001
type = preference
content = "User usually prefers cheaper flights."
```

Later:

```text
I hate overnight layovers.
```

Stored:

```text
M002
type = preference
content = "Avoid overnight layovers."
```

Optional third memory:

```text
M003
type = preference
content = "Economy class is fine."
```

---

## Session 2 — Action

User:

```text
Book me a flight to Tokyo next Friday.
```

Available options:

```text
Flight A
$320
2 stops
overnight layover

Flight B
$390
direct
daytime

Flight C
$355
1 stop
no overnight layover
```

The agent selects:

```text
Flight A
```

This creates an incident because the user had explicitly said they dislike overnight layovers.

---

## Incident

Display:

```text
INCIDENT #I001

Unexpected action:
Flight A selected

Possible memory influence:
M001
M002
M003
```

---

## Original Replay

Replay using the exact original context:

```text
M001 + M002 + M003
```

Nemotron result:

```text
Flight A
```

This confirms the incident is reproducible.

---

## Counterfactual Replay

Replay without M001:

```text
M002 + M003
```

Nemotron result:

```text
Flight B
```

Replay without M002:

```text
M001 + M003
```

Nemotron result:

```text
Flight A
```

Replay without M003:

```text
M001 + M002
```

Nemotron result:

```text
Flight A
```

Conclusion:

```text
M001 materially changed the decision.
```

---

## Remediation

User selects:

```text
Quarantine M001
```

Memory becomes:

```text
status = QUARANTINED
```

Future decision:

```text
Book me a flight to Tokyo next Friday.
```

Agent now excludes M001.

Result:

```text
Flight B
```

This closes the full loop:

```text
Incident
↓
Replay
↓
Counterfactual
↓
Memory attribution
↓
Quarantine
↓
Changed future behavior
```

---

# 5. Critical Competition Rule

Nemotron must be used for the replay reasoning itself.

Do NOT build:

```text
Python decides the replay result
↓
Nemotron writes the explanation
```

Required:

```text
Replay Context
↓
Nebius Token Factory
↓
Nemotron
↓
Structured Action Decision
```

For every counterfactual run:

```text
Modified Memory Set
↓
Nemotron
↓
Action Decision
```

Then the application compares results.

---

# 6. Architecture

```text
┌───────────────────────────────┐
│      Web UI / Next.js        │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│        FastAPI Backend        │
│                               │
│ Session / Memory / Incident   │
└───────────────┬───────────────┘
                │
       ┌────────┼──────────────┐
       │        │              │
       ▼        ▼              ▼
   Memory DB  Replay Engine  Incident Store
       │        │
       │        ▼
       │   Nebius Token Factory
       │        │
       │        ▼
       │      Nemotron
       │        │
       └────────┼──────────────
                ▼
      Counterfactual Comparator
                │
                ▼
      Attribution / Remediation
                │
                ▼
       Quarantine Memory
```

---

# 7. Suggested Tech Stack

## Frontend

```text
Next.js
TypeScript
Tailwind CSS
```

## Backend

```text
Python 3.12
FastAPI
Pydantic
SQLAlchemy
```

## Database

MVP:

```text
SQLite
```

Later:

```text
PostgreSQL
```

## Model Runtime

Required:

```text
Nebius Token Factory
+
Nemotron
```

## Testing

```text
pytest
Playwright
```

## Demo Recording

```text
Playwright
FFmpeg
```

---

# 8. Repository Structure

```text
recallguard/
├── frontend/
│   ├── app/
│   ├── components/
│   ├── lib/
│   └── types/
│
├── backend/
│   ├── main.py
│   ├── api/
│   │   ├── sessions.py
│   │   ├── memories.py
│   │   ├── incidents.py
│   │   ├── replay.py
│   │   └── remediation.py
│   ├── agent/
│   │   ├── personal_agent.py
│   │   ├── prompts.py
│   │   └── decision_schema.py
│   ├── replay/
│   │   ├── engine.py
│   │   ├── counterfactual.py
│   │   ├── comparator.py
│   │   └── attribution.py
│   ├── nebius/
│   │   ├── client.py
│   │   ├── models.py
│   │   └── token_factory.py
│   ├── memory/
│   │   ├── repository.py
│   │   ├── models.py
│   │   └── selector.py
│   ├── incidents/
│   │   ├── recorder.py
│   │   └── models.py
│   ├── db/
│   │   ├── database.py
│   │   └── schema.py
│   └── tests/
│       ├── test_memory_persistence.py
│       ├── test_original_replay.py
│       ├── test_counterfactual_replay.py
│       ├── test_attribution.py
│       └── test_quarantine.py
├── data/
│   ├── flights.json
│   └── demo-seed.json
├── demo/
│   ├── demo-recording.spec.ts
│   └── narration.json
├── docs/
│   ├── architecture.md
│   ├── demo-script.md
│   ├── product-feedback.md
│   ├── friction-log.md
│   └── devpost.md
├── scripts/
│   ├── install.sh
│   ├── start.sh
│   ├── stop.sh
│   ├── test.sh
│   ├── seed-demo.sh
│   └── record-demo.sh
├── .env.example
├── README.md
└── LICENSE
```

---

# 9. Data Models

## User

```text
id
name
created_at
```

## Session

```text
id
user_id
created_at
```

## Memory

```text
id
user_id
type
content
status
created_at
source_session_id
```

status:

```text
ACTIVE
QUARANTINED
REVOKED
```

## DecisionRequest

```text
id
session_id
user_message
task_type
options_json
created_at
```

## Decision

```text
id
request_id
selected_option_id
reasoning_summary
model_name
model_provider
created_at
```

Do not store hidden chain-of-thought.

Store only:

```text
reasoning_summary
decision factors
structured output
```

## Incident

```text
id
decision_id
incident_type
description
status
created_at
```

## ReplaySnapshot

This is critical.

```text
id
incident_id
user_message
options_json
memory_ids
model_name
prompt_version
system_prompt_hash
created_at
```

Purpose:

> Reproduce the original decision context.

## ReplayRun

```text
id
snapshot_id
run_type
removed_memory_id
modified_memory_id
selected_option_id
reasoning_summary
model_name
latency_ms
created_at
```

run_type:

```text
ORIGINAL
REMOVE_MEMORY
MODIFY_MEMORY
NO_MEMORY
```

## AttributionResult

```text
id
incident_id
memory_id
original_action
counterfactual_action
action_changed
attribution_score
status
created_at
```

---

# 10. Structured Nemotron Output

Request Nemotron to return JSON:

```json
{
  "selected_option_id": "FLIGHT_A",
  "decision_factors": [
    "lower price",
    "economy acceptable"
  ],
  "memory_ids_used": [
    "M001",
    "M003"
  ],
  "confidence": 0.82,
  "summary": "Selected the cheapest option because the user's stored preferences emphasized lower cost."
}
```

Important:

`memory_ids_used` is model-reported evidence, not proof.

Counterfactual action change is stronger evidence.

---

# 11. Original Agent Prompt

Conceptual template:

```text
You are a personal assistant.

User request:
{user_request}

Available options:
{options}

Relevant user memories:
{memories}

Select exactly one option.

Return structured JSON only:
- selected_option_id
- decision_factors
- memory_ids_used
- confidence
- summary
```

---

# 12. Replay Engine

## Original Replay

Input:

```text
same user request
same available options
same memory snapshot
same prompt version
same model
```

Output:

```text
selected option
```

Goal:

```text
original action == replay action
```

If replay cannot reproduce the original:

```text
REPLAY_UNSTABLE
```

Do not claim counterfactual attribution is reliable.

---

# 13. Counterfactual Replay Algorithm

Given:

```text
memories = [M001, M002, M003]
```

Run:

```text
R0 = all memories
R1 = without M001
R2 = without M002
R3 = without M003
```

Pseudo:

```python
original = replay(all_memories)

for memory in memories:
    modified = all_memories - {memory}
    result = replay(modified)

    changed = result.action != original.action

    save_counterfactual(memory, changed, result)
```

---

# 14. Attribution Logic

MVP:

```text
action changed → HIGH influence
action unchanged → LOW influence
```

More detailed:

```text
HIGH
Action changes to a materially different option.

MEDIUM
Same action but decision factors change significantly.

LOW
Action and major factors remain unchanged.
```

Avoid calling this definitive causality.

Use:

```text
counterfactual contribution
decision influence
material influence
```

Avoid:

```text
proven causal cause
```

unless stronger experimental controls exist.

---

# 15. Replay Stability

LLM outputs can vary.

Recommended MVP:

```text
3 runs per condition
```

Example:

```text
Original:
Flight A
Flight A
Flight A

Without M001:
Flight B
Flight B
Flight B
```

Strong evidence.

If:

```text
Flight A
Flight B
Flight A
```

mark:

```text
UNSTABLE
```

---

# 16. Attribution Score

Simple version:

```text
score =
number_of_counterfactual_runs_that_changed_action
/
total_counterfactual_runs
```

Example:

```text
Without M001

3 / 3 changed
→ 1.00
→ HIGH
```

Without M002:

```text
0 / 3 changed
→ 0.00
→ LOW
```

---

# 17. Quarantine Flow

UI button:

```text
Quarantine Memory
```

API:

```text
POST /api/memories/{id}/quarantine
```

Update:

```text
status = QUARANTINED
```

Memory selector must exclude:

```text
QUARANTINED
REVOKED
```

from future decisions.

---

# 18. API Specification

## POST /api/session
Create session.

## POST /api/memory

Request:

```json
{
  "content": "User usually prefers cheaper flights.",
  "type": "preference"
}
```

## GET /api/memories
Return current memories.

## POST /api/agent/decide

Request:

```json
{
  "session_id": "S002",
  "message": "Book me a flight to Tokyo next Friday."
}
```

Response:

```json
{
  "decision_id": "D001",
  "selected_option_id": "FLIGHT_A",
  "memory_ids_used": ["M001", "M003"]
}
```

## POST /api/incidents
Create incident from decision.

## POST /api/incidents/{id}/replay
Run original replay.

## POST /api/incidents/{id}/counterfactual
Run all single-memory removals.

## GET /api/incidents/{id}/attribution
Return ranked memory influence.

## POST /api/memories/{id}/quarantine
Quarantine memory.

---

# 19. Frontend Pages

First version only needs 4 screens.

## Screen 1 — Personal AI

Show:

```text
Chat
Current memories
Current session
```

## Screen 2 — Decision

Show:

```text
User Request
Available Flights
Selected:
Flight A

Memories Available:
M001
M002
M003
```

Button:

```text
Report Incident
```

## Screen 3 — Replay Lab

Show:

```text
Original Replay
Counterfactual Replays
```

Table:

| Condition | Result | Changed? |
|---|---|---|
| All memories | Flight A | baseline |
| Without M001 | Flight B | YES |
| Without M002 | Flight A | NO |
| Without M003 | Flight A | NO |

## Screen 4 — Memory Review

Show:

```text
M001

"User usually prefers cheaper flights."

Influence:
HIGH

Counterfactual score:
1.00
```

Button:

```text
Quarantine
```

---

# 20. Nebius Client

Create:

```text
backend/nebius/client.py
```

Environment:

```text
NEBIUS_API_KEY=
NEBIUS_MODEL=
NEBIUS_BASE_URL=
```

Do not commit secrets.

Add:

```text
.env.example
```

---

# 21. Phase 0 — Smoke Test

Create:

```text
scripts/nebius-smoke-test.py
```

It must:

```text
1. Load API key
2. Call Token Factory
3. Call selected Nemotron model
4. Request structured JSON
5. Validate response
6. Print latency
```

Done condition:

```text
Nemotron successfully returns a valid decision.
```

No further product work until this passes.

---

# 22. Development Order

Strict order:

## Phase 0
Nebius + Nemotron smoke test

## Phase 1
Database + memories

## Phase 2
Static flight dataset

## Phase 3
Nemotron decision API

## Phase 4
Incident snapshot

## Phase 5
Original replay

## Phase 6
Single-memory counterfactual replay

## Phase 7
Attribution score

## Phase 8
Quarantine

## Phase 9
Frontend

## Phase 10
Automated tests

## Phase 11
Playwright demo

## Phase 12
README / Devpost / feedback

---

# 23. Gate Conditions

## Gate 0

If Token Factory / Nemotron cannot be called:

> Stop.

Do not replace with another model and still claim competition compliance.

## Gate 1

Original replay must reproduce the original action reliably.

If not:

```text
Replay Stability = FAIL
```

Do not continue attribution.

## Gate 2

At least one controlled memory must produce a measurable counterfactual action change.

If no memory removal changes the action:

> Rewrite the demo scenario.

Do not fake attribution.

## Gate 3

Quarantine must change future memory selection.

---

# 24. Tests

Minimum automated tests:

```text
test_memory_persists_across_sessions
test_quarantined_memory_is_excluded
test_snapshot_contains_exact_memory_ids
test_original_replay_reproduces_action
test_remove_m001_changes_action
test_remove_m002_does_not_change_action
test_attribution_score
test_unstable_replay_flag
test_incident_trace
test_nebius_response_schema
```

---

# 25. Model Output Validation

Never trust raw model output.

Use Pydantic:

```text
DecisionOutput
```

Fields:

```text
selected_option_id
decision_factors
memory_ids_used
confidence
summary
```

Validate:

```text
selected_option_id exists
memory ids exist
confidence 0–1
no unknown option
```

---

# 26. Demo Seed

Create deterministic seed:

```text
User:
Demo User

Memories:
M001 cheaper flights
M002 avoid overnight layovers
M003 economy is fine

Flights:
A / B / C
```

Reset:

```text
POST /api/demo/reset
```

---

# 27. 3-Minute Demo Script

## 0:00–0:20 — Problem

> Personal AI gets better by remembering us. But what happens when the wrong memory influences a future action?

## 0:20–0:40 — Memories

```text
M001 Cheaper flights
M002 Avoid overnight layovers
M003 Economy is fine
```

## 0:40–1:00 — Bad Decision

```text
Book me a flight to Tokyo next Friday.
```

Agent:

```text
Flight A
$320
Overnight layover
```

## 1:00–1:15 — Incident

Click:

```text
Report Incident
```

## 1:15–1:35 — Original Replay

```text
Nemotron Replay
All memories
→ Flight A
```

## 1:35–2:00 — Counterfactual

```text
Without M001
→ Flight B

Without M002
→ Flight A

Without M003
→ Flight A
```

Highlight:

```text
M001 = HIGH influence
```

## 2:00–2:20 — Quarantine

Click:

```text
Quarantine M001
```

## 2:20–2:40 — Future Decision

Run same task.

Result:

```text
Flight B
```

## 2:40–3:00 — Closing

> Personal AI should not only remember. It should be able to show which memory changed its behavior.

---

# 28. Playwright Recording

Create:

```text
demo/demo-recording.spec.ts
```

Workflow:

```text
Reset
↓
Show memories
↓
Run bad decision
↓
Report incident
↓
Original replay
↓
Counterfactual replay
↓
Quarantine M001
↓
Run again
↓
Show changed action
```

Output:

```text
artifacts/recallguard-demo.webm
```

---

# 29. README Structure

```text
# RecallGuard

## One-line pitch
## Problem
## Why Personal AI
## What We Built
## Demo
## Architecture
## How Counterfactual Replay Works
## Nemotron Integration
## Replay Stability
## Memory Attribution
## Quarantine
## Setup
## Environment Variables
## Tests
## Demo Recording
## Product Feedback
## Friction Log
## Limitations
## What Was Built for This Hackathon
## Future Work
```

---

# 30. Devpost About Structure

Use:

```text
## Inspiration
## What it does
## How we built it
## Challenges we ran into
## Accomplishments that we're proud of
## What we learned
## What's next
```

---

# 31. Product Feedback

Create from day one:

```text
docs/product-feedback.md
```

Track:

```text
Nebius Token Factory
Nemotron model
API onboarding
latency
structured outputs
rate limits
documentation
error handling
model quality
```

Do not write feedback only at the end.

---

# 32. Friction Log

Create:

```text
docs/friction-log.md
```

Template:

| Task | Steps | Expected | Actual | Severity | Workaround | Suggestion |
|---|---|---|---|---|---|---|

Record real issues only.

---

# 33. MVP Completion Checklist

- [ ] Token Factory smoke test passes
- [ ] Nemotron returns valid structured output
- [ ] Memories persist across sessions
- [ ] Flight decision uses active memories
- [ ] Incident snapshot saved
- [ ] Original replay works
- [ ] Counterfactual replay works
- [ ] M001 removal changes action
- [ ] Attribution score computed
- [ ] Memory can be quarantined
- [ ] Quarantined memory excluded
- [ ] Future action changes
- [ ] Tests pass
- [ ] Demo reset works
- [ ] Video can be recorded automatically

---

# 34. Contender Completion Checklist

- [ ] Nemotron is clearly the replay engine
- [ ] Replay trace visible in UI
- [ ] Model name visible
- [ ] Latency visible
- [ ] Replay stability visible
- [ ] Counterfactual results ranked
- [ ] Human remediation visible
- [ ] Product feedback complete
- [ ] Friction log complete
- [ ] README competition-ready
- [ ] 3-minute demo polished
- [ ] Public GitHub repo
- [ ] Open-source license

---

# 35. Do Not Build Yet

Do not add:

```text
multi-agent fleet
blast radius
restore checkpoint
full causal graph
enterprise SRE dashboard
calendar integration
email integration
real travel booking
vector DB
knowledge graph
local model fallback
multiple incidents
```

until the core counterfactual demo works.

---

# 36. Claude IDE First Prompt

```text
Read this specification completely before writing code.

Implement Phase 0 through Phase 3 only.

Do not build the frontend yet.

Tech stack:
- Python 3.12
- FastAPI
- SQLAlchemy
- SQLite
- Nebius Token Factory
- Nemotron

First milestone:
1. Create repository structure.
2. Add .env.example.
3. Implement a Token Factory / Nemotron smoke test.
4. Seed the demo flight dataset.
5. Implement persistent Memory storage.
6. Implement a Nemotron decision function that returns validated structured JSON.
7. Add tests.

Critical rule:
Nemotron must make the decision from the supplied memory context.
Do not simulate or hard-code the model decision.

Stop after Phase 3 and report:
- files created
- commands to run
- tests
- smoke-test result
- unresolved issues
```

---

# 37. Claude IDE Second Prompt

```text
Implement Phase 4 through Phase 8.

Add:
- incident snapshot
- original replay
- counterfactual memory removal
- 3 repeated runs per condition
- replay stability
- attribution score
- quarantine flow

Do not build the frontend yet.

Critical rule:
Counterfactual results must come from real Nemotron inference calls.
Do not hard-code expected outcomes.

If the demo scenario does not produce a stable action change when M001 is removed, report that clearly and adjust only the seed scenario or prompt design.
Do not fake attribution.
```

---

# 38. Claude IDE Third Prompt

```text
Implement the frontend and automated demo.

Use:
- Next.js
- TypeScript
- Tailwind CSS
- Playwright

Build only four main screens:
1. Personal AI
2. Decision
3. Replay Lab
4. Memory Review

Add Reset Demo.

Create a Playwright recording script that runs the complete demo in under 3 minutes.

Do not add unrelated product features.
```

---

# 39. Final Technical Message

```text
Persistent Memory
↓
Personal AI Decision
↓
Incident
↓
Nemotron Replay
↓
Remove One Memory
↓
Nemotron Replay Again
↓
Action Difference
↓
Memory Influence
↓
Human Quarantine
```

Final tagline:

> **Find the memory that changed the agent's mind.**
