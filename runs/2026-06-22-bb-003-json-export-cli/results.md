# BB-003 — JSON export for existing CLI results

Feature addition: add stable JSON export while preserving text UX; differentiates process and implementation discipline more than BB-001.

## Verification summary

| Agent | Verdict | Wall | Agent exit | Verify exit | Patch | Execution |
|---|---:|---:|---:|---:|---:|---:|
| OpenCode | PASS | 66.732s | n/a | n/a | 100 | 66 |
| Claude | PASS | 52.901s | n/a | n/a | 100 | 68 |
| MiMo | PASS | 94.151s | n/a | n/a | 100 | 53 |
| Pi | PASS | 56.314s | n/a | n/a | 100 | 74 |
| Codex | PASS | 104.966s | n/a | n/a | 100 | 66 |
| agy | PASS | 147.780s | n/a | n/a | 100 | 44 |

## Evidence

Each agent has committed-style artifacts under `agents/<agent>/`:

- `agent.log`
- `agent-meta.txt`
- `diff.patch`
- `git-status.txt`
- `verify.log`
- `result.json`

Baseline failure is stored at `evidence/baseline-failure.log`.
