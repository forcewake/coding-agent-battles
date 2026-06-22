# BB-002 — CSV edge-case parser results

CSV parser edge cases: quoted commas, escaped quotes, blank rows, deterministic grouping.

## Verification summary

| Agent | Verdict | Wall | Agent exit | Verify exit | Patch | Process |
|---|---:|---:|---:|---:|---:|---:|
| OpenCode | PASS | 80.638s | 0 | 0 | 100 | 90 |
| Claude | PASS | 93.744s | 0 | 0 | 100 | 90 |
| MiMo | PASS | 66.505s | 0 | 0 | 100 | 90 |
| Pi | PASS | 125.715s | 0 | 0 | 100 | 90 |
| Codex | PASS | 101.812s | 0 | 0 | 100 | 90 |
| agy | PASS | 202.767s | 0 | 0 | 100 | 90 |

## Evidence

Each agent has committed-style artifacts under `agents/<agent>/`:

- `agent.log`
- `agent-meta.txt`
- `diff.patch`
- `git-status.txt`
- `verify.log`
- `result.json`

Baseline failure is stored at `evidence/baseline-failure.log`.
