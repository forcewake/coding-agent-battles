# BB-009 — Observability instrumentation results

Add safe structured request events with correlation IDs and no secret logging.

## Verification summary

| Agent | Verdict | Wall | Agent exit | Verify exit | Patch | Execution |
|---|---:|---:|---:|---:|---:|---:|
| OpenCode | PASS | 58.357s | 0 | 0 | 100 | 97 |
| Claude | PASS | 89.627s | 0 | 0 | 100 | 92 |
| MiMo | PASS | 91.989s | 0 | 0 | 100 | 92 |
| Pi | PASS | 68.880s | 0 | 0 | 100 | 96 |
| Codex | PASS | 100.717s | 0 | 0 | 100 | 90 |
| agy | FAIL | 43.784s | 0 | 1 | 0 | 30 |

## Evidence

Each agent has committed-style artifacts under `agents/<agent>/`:

- `agent.log`
- `agent-meta.txt`
- `diff.patch`
- `git-status.txt`
- `verify.log`
- `result.json`

Baseline failure is stored at `evidence/baseline-failure.log`.
