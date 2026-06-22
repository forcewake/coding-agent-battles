# BB-002 — CSV edge-case parser results

CSV parser edge cases: quoted commas, escaped quotes, blank rows, deterministic grouping.

## Verification summary

| Agent | Verdict | Wall | Agent exit | Verify exit | Patch | Execution |
|---|---:|---:|---:|---:|---:|---:|
| OpenCode | PASS | 80.638s | 0 | 0 | 100 | 92 |
| Claude | PASS | 93.744s | 0 | 0 | 100 | 86 |
| MiMo | PASS | 66.505s | 0 | 0 | 100 | 85 |
| Pi | PASS | 125.715s | 0 | 0 | 100 | 93 |
| Codex | PASS | 101.812s | 0 | 0 | 100 | 85 |
| agy | PASS | 202.767s | 0 | 0 | 100 | 69 |

## Evidence

Each agent has committed-style artifacts under `agents/<agent>/`:

- `agent.log`
- `agent-meta.txt`
- `diff.patch`
- `git-status.txt`
- `verify.log`
- `result.json`

Baseline failure is stored at `evidence/baseline-failure.log`.
