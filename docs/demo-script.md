# Demo script (≈95 s automated, ≤ 3:00 budget)

Run: `scripts/record-demo.sh` → `artifacts/recallguard-demo.webm`. Captions: [demo/narration.json](../demo/narration.json).

| Time | Screen | Beat |
|---|---|---|
| 0:00 | Personal AI | Problem: wrong memory changes behavior |
| 0:06 | Personal AI | M001 cheapest · M002 avoid overnight · M003 economy fine |
| 0:20 | Decision | "Book me a flight to Tokyo next Friday." → Nemotron picks **Flight A** (overnight) |
| 0:35 | Decision | Report Incident → snapshot frozen |
| 0:40 | Replay Lab | Original replay 3× → Flight A, STABLE |
| 0:50 | Replay Lab | Counterfactual: without M001 → C; without M002/M003 → A |
| 1:10 | Memory Review | M001 HIGH, score 1.00 → Quarantine |
| 1:20 | Memory Review | Run again → Flight C, M001 excluded |
| 1:30 | — | "Find the memory that changed the agent's mind." |

Manual run: `scripts/start.sh` → http://localhost:3000 → click through tabs 1→4.
