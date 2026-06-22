# BB-008 — Monorepo dependency upgrade results

Adapt app package to upgraded shared slug API without reintroducing legacy export.

## Verification summary

| Agent | Verdict | Wall | Agent exit | Verify exit | Patch | Execution |
|---|---:|---:|---:|---:|---:|---:|
| OpenCode | PASS | 42.590s | 0 | 0 | 100 | 98 |
| Claude | PASS | 34.085s | 0 | 0 | 100 | 100 |
| MiMo | PASS | 42.267s | 0 | 0 | 100 | 98 |
| Pi | PASS | 54.993s | 0 | 0 | 100 | 96 |
| Codex | PASS | 82.653s | 0 | 0 | 100 | 90 |
| agy | PASS | 34.446s | 0 | 0 | 100 | 100 |

## Evidence

Each agent has committed-style artifacts under `agents/<agent>/`:

- `agent.log`
- `agent-meta.txt`
- `diff.patch`
- `git-status.txt`
- `verify.log`
- `result.json`

Baseline failure is stored at `evidence/baseline-failure.log`.
