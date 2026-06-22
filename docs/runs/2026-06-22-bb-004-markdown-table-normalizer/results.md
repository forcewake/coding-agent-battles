# BB-004 — Markdown table normalizer results

Normalize Markdown pipe tables with padded columns and idempotent output.

## Verification summary

| Agent | Verdict | Wall | Agent exit | Verify exit | Patch | Execution |
|---|---:|---:|---:|---:|---:|---:|
| OpenCode | PASS | 167.030s | 0 | 0 | 100 | 92 |
| Claude | PASS | 169.013s | 0 | 0 | 100 | 88 |
| MiMo | PASS | 190.220s | 0 | 0 | 100 | 82 |
| Pi | PASS | 247.114s | 0 | 0 | 100 | 85 |
| Codex | PASS | 219.382s | 0 | 0 | 100 | 73 |
| agy | PASS | 113.300s | 0 | 0 | 100 | 84 |

## Evidence

Each agent has committed-style artifacts under `agents/<agent>/`:

- `agent.log`
- `agent-meta.txt`
- `diff.patch`
- `git-status.txt`
- `verify.log`
- `result.json`

Baseline failure is stored at `evidence/baseline-failure.log`.
