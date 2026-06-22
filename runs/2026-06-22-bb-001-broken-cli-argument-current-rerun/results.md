# BB-001 — Broken CLI argument results

Fix wordfreq --min-length parsing while preserving default word count output.

## Verification summary

| Agent | Verdict | Wall | Agent exit | Verify exit | Patch | Execution |
|---|---:|---:|---:|---:|---:|---:|
| OpenCode | PASS | 94.645s | 0 | 0 | 100 | 96 |
| Claude | PASS | 53.025s | 0 | 0 | 100 | 100 |
| MiMo | PASS | 64.559s | 0 | 0 | 100 | 99 |
| Pi | PASS | 119.437s | 0 | 0 | 100 | 93 |
| Codex | PASS | 147.902s | 0 | 0 | 100 | 90 |
| agy | PASS | 51.705s | 0 | 0 | 100 | 100 |

## Evidence

Each agent has committed-style artifacts under `agents/<agent>/`:

- `agent.log`
- `agent-meta.txt`
- `diff.patch`
- `git-status.txt`
- `verify.log`
- `result.json`

Baseline failure is stored at `evidence/baseline-failure.log`.
