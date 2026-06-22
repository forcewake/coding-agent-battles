# BB-006 — React filter/search UI results

Browser-visible search/filter state model with stable empty-state copy.

## Verification summary

| Agent | Verdict | Wall | Agent exit | Verify exit | Patch | Process |
|---|---:|---:|---:|---:|---:|---:|
| OpenCode | PASS | 34.886s | 0 | 0 | 100 | 90 |
| Claude | PASS | 93.299s | 0 | 0 | 100 | 90 |
| MiMo | PASS | 39.162s | 0 | 0 | 100 | 90 |
| Pi | PASS | 54.147s | 0 | 0 | 100 | 90 |
| Codex | PASS | 79.096s | 0 | 0 | 100 | 90 |
| agy | PASS | 37.526s | 0 | 0 | 100 | 90 |

## Evidence

Each agent has committed-style artifacts under `agents/<agent>/`:

- `agent.log`
- `agent-meta.txt`
- `diff.patch`
- `git-status.txt`
- `verify.log`
- `result.json`

Baseline failure is stored at `evidence/baseline-failure.log`.
