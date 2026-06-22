# BB-007 — SQLite migration with rollback results

Safe SQLite upgrade/downgrade preserving rows and idempotent upgrade behavior.

## Verification summary

| Agent | Verdict | Wall | Agent exit | Verify exit | Patch | Execution |
|---|---:|---:|---:|---:|---:|---:|
| OpenCode | PASS | 48.124s | 0 | 0 | 100 | 98 |
| Claude | PASS | 86.768s | 0 | 0 | 100 | 79 |
| MiMo | PASS | 82.405s | 0 | 0 | 100 | 79 |
| Pi | PASS | 137.179s | 0 | 0 | 100 | 85 |
| Codex | PASS | 122.860s | 0 | 0 | 100 | 74 |
| agy | PASS | 74.759s | 0 | 0 | 100 | 79 |

## Evidence

Each agent has committed-style artifacts under `agents/<agent>/`:

- `agent.log`
- `agent-meta.txt`
- `diff.patch`
- `git-status.txt`
- `verify.log`
- `result.json`

Baseline failure is stored at `evidence/baseline-failure.log`.
