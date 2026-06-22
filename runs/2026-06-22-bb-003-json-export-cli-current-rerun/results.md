# BB-003 — JSON export for existing CLI results

Feature addition: add stable JSON export while preserving text UX.

## Verification summary

| Agent | Verdict | Wall | Agent exit | Verify exit | Patch | Execution |
|---|---:|---:|---:|---:|---:|---:|
| OpenCode | PASS | 69.014s | 0 | 0 | 100 | 94 |
| Claude | PASS | 80.125s | 0 | 0 | 100 | 93 |
| MiMo | PASS | 63.405s | 0 | 0 | 100 | 95 |
| Pi | PASS | 94.955s | 0 | 0 | 100 | 91 |
| Codex | PASS | 103.024s | 0 | 0 | 100 | 90 |
| agy | PASS | 19.505s | 0 | 0 | 100 | 100 |

## Evidence

Each agent has committed-style artifacts under `agents/<agent>/`:

- `agent.log`
- `agent-meta.txt`
- `diff.patch`
- `git-status.txt`
- `verify.log`
- `result.json`

Baseline failure is stored at `evidence/baseline-failure.log`.
