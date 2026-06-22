# BB-007 — SQLite migration with rollback results

Safe SQLite upgrade/downgrade preserving rows and idempotent upgrade behavior.

## Verification summary

| Agent | Verdict | Wall | Agent exit | Verify exit | Patch | Process |
|---|---:|---:|---:|---:|---:|---:|
| OpenCode | PASS | 48.124s | 0 | 0 | 100 | 90 |
| Claude | PASS | 86.768s | 0 | 0 | 100 | 90 |
| MiMo | PASS | 82.405s | 0 | 0 | 100 | 90 |
| Pi | PASS | 137.179s | 0 | 0 | 100 | 90 |
| Codex | PASS | 122.860s | 0 | 0 | 100 | 90 |
| agy | PASS | 74.759s | 0 | 0 | 100 | 90 |

## Evidence

Each agent has committed-style artifacts under `agents/<agent>/`:

- `agent.log`
- `agent-meta.txt`
- `diff.patch`
- `git-status.txt`
- `verify.log`
- `result.json`

Baseline failure is stored at `evidence/baseline-failure.log`.
