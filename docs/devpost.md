# Devpost — RecallGuard

## Inspiration
Personal AI gets better by remembering us — until a stale or over-weighted memory quietly drives a bad action and nobody can say which one.

## What it does
When the assistant makes a bad decision, RecallGuard freezes the exact memory context, has **Nemotron** replay it, removes one memory at a time and replays again, then reports which memory changed the action (counterfactual score). A human quarantines the culprit and the next decision changes.

## How we built it
Python/FastAPI + SQLite backend, Next.js UI (4 screens), Nebius Token Factory + `nvidia/nemotron-3-super-120b-a12b`. Every decision and every replay is a real Nemotron call through one shared code path; comparison and scoring are deterministic code. 3 repeats per condition, stability flag, gates that refuse to fake attribution. Playwright records the demo automatically.

## Challenges we ran into
- The first scenario never produced the bad decision: Nemotron honoured "avoid overnight layovers". We tuned memory wording against the real model instead of hard-coding results.
- Temperature 0 was not fully deterministic → repeat-and-vote + UNSTABLE state.

## Accomplishments that we're proud of
A closed loop — incident → replay → counterfactual → attribution → quarantine → changed behavior — verified end-to-end against live Nemotron (M001 removal 3/3 changes action; M002/M003 0/3).

## What we learned
How strongly memory phrasing steers a personal agent, and that replay needs stability checks to be trustworthy.

## What's next
Pairwise/joint removal, MODIFY_MEMORY runs, more scenarios, factor-level (MEDIUM) influence, Postgres.
