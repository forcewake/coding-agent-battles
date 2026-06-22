# BB-004 — Markdown table normalizer results

Normalize Markdown pipe tables with padded columns and idempotent output.

## Verification summary

| Agent | Verdict | Wall | Agent exit | Verify exit | Patch | Process |
|---|---:|---:|---:|---:|---:|---:|
| OpenCode | PASS | 167.030s | 0 | 0 | 100 | 90 |
| Claude | PASS | 169.013s | 0 | 0 | 100 | 90 |
| MiMo | PASS | 190.220s | 0 | 0 | 100 | 90 |
| Pi | PASS | 247.114s | 0 | 0 | 100 | 90 |
| Codex | PASS | 219.382s | 0 | 0 | 100 | 90 |
| agy | PASS | 113.300s | 0 | 0 | 100 | 90 |

## Evidence

Each agent has committed-style artifacts under `agents/<agent>/`:

- `agent.log`
- `agent-meta.txt`
- `diff.patch`
- `git-status.txt`
- `verify.log`
- `result.json`

Baseline failure is stored at `evidence/baseline-failure.log`.
