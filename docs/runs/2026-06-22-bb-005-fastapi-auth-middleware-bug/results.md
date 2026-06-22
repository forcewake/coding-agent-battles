# BB-005 — FastAPI auth middleware bug results

Fix FastAPI auth dependency so admin is protected while health remains public.

## Verification summary

| Agent | Verdict | Wall | Agent exit | Verify exit | Patch | Execution |
|---|---:|---:|---:|---:|---:|---:|
| OpenCode | PASS | 43.633s | 0 | 0 | 100 | 99 |
| Claude | PASS | 47.969s | 0 | 0 | 100 | 91 |
| MiMo | PASS | 46.894s | 0 | 0 | 100 | 93 |
| Pi | PASS | 87.805s | 0 | 0 | 100 | 88 |
| Codex | PASS | 100.380s | 0 | 0 | 100 | 70 |
| agy | FAIL | 47.220s | 0 | 1 | 0 | 33 |

## Evidence

Each agent has committed-style artifacts under `agents/<agent>/`:

- `agent.log`
- `agent-meta.txt`
- `diff.patch`
- `git-status.txt`
- `verify.log`
- `result.json`

Baseline failure is stored at `evidence/baseline-failure.log`.
