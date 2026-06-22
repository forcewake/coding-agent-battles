# BB-006 — React filter/search UI results

Browser-visible search/filter state model with stable empty-state copy.

## Verification summary

| Agent | Verdict | Wall | Agent exit | Verify exit | Patch | Execution |
|---|---:|---:|---:|---:|---:|---:|
| OpenCode | PASS | 34.886s | 0 | 0 | 100 | 97 |
| Claude | PASS | 93.299s | 0 | 0 | 100 | 72 |
| MiMo | PASS | 39.162s | 0 | 0 | 100 | 87 |
| Pi | PASS | 54.147s | 0 | 0 | 100 | 95 |
| Codex | PASS | 79.096s | 0 | 0 | 100 | 74 |
| agy | PASS | 37.526s | 0 | 0 | 100 | 83 |

## Evidence

Each agent has committed-style artifacts under `agents/<agent>/`:

- `agent.log`
- `agent-meta.txt`
- `diff.patch`
- `git-status.txt`
- `verify.log`
- `result.json`

Baseline failure is stored at `evidence/baseline-failure.log`.
