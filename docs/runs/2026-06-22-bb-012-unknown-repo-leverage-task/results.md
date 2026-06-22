# BB-012 — Unknown repo leverage task results

Use provided vendor text helper instead of reimplementing tokenization incorrectly.

## Verification summary

| Agent | Verdict | Wall | Agent exit | Verify exit | Patch | Process |
|---|---:|---:|---:|---:|---:|---:|
| OpenCode | PASS | 52.259s | 0 | 0 | 100 | 90 |
| Claude | PASS | 43.710s | 0 | 0 | 100 | 90 |
| MiMo | PASS | 64.967s | 0 | 0 | 100 | 90 |
| Pi | PASS | 86.329s | 0 | 0 | 100 | 90 |
| Codex | PASS | 90.124s | 0 | 0 | 100 | 90 |
| agy | PASS | 102.463s | 0 | 0 | 100 | 90 |

## Evidence

Each agent has committed-style artifacts under `agents/<agent>/`:

- `agent.log`
- `agent-meta.txt`
- `diff.patch`
- `git-status.txt`
- `verify.log`
- `result.json`

Baseline failure is stored at `evidence/baseline-failure.log`.
