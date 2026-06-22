# BB-009 — Observability instrumentation results

Add safe structured request events with correlation IDs and no secret logging.

## Verification summary

| Agent | Verdict | Wall | Agent exit | Verify exit | Patch | Execution |
|---|---:|---:|---:|---:|---:|---:|
| OpenCode | PASS | 58.357s | 0 | 0 | 100 | 92 |
| Claude | PASS | 89.627s | 0 | 0 | 100 | 80 |
| MiMo | PASS | 91.989s | 0 | 0 | 100 | 72 |
| Pi | PASS | 68.880s | 0 | 0 | 100 | 93 |
| Codex | PASS | 100.717s | 0 | 0 | 100 | 75 |
| agy | FAIL | 43.784s | 0 | 1 | 0 | 34 |

## Evidence

Each agent has committed-style artifacts under `agents/<agent>/`:

- `agent.log`
- `agent-meta.txt`
- `diff.patch`
- `git-status.txt`
- `verify.log`
- `result.json`

Baseline failure is stored at `evidence/baseline-failure.log`.
