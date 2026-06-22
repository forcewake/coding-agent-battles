# BB-001 — Broken CLI argument results

Calibration bugfix: one broken argparse flag; proves red baseline, isolation, telemetry and verification plumbing.

## Verification summary

| Agent | Verdict | Wall | Agent exit | Verify exit | Patch | Execution |
|---|---:|---:|---:|---:|---:|---:|
| OpenCode | PASS | 35.587s | n/a | n/a | 100 | 73 |
| Claude | PASS | 40.680s | n/a | n/a | 100 | 59 |
| MiMo | PASS | 63.621s | n/a | n/a | 100 | 57 |
| Pi | PASS | 70.733s | n/a | n/a | 100 | 82 |
| Codex | PASS | 114.752s | n/a | n/a | 100 | 52 |
| agy | PASS | 191.826s | n/a | n/a | 100 | 44 |

## Evidence

Each agent has committed-style artifacts under `agents/<agent>/`:

- `agent.log`
- `agent-meta.txt`
- `diff.patch`
- `git-status.txt`
- `verify.log`
- `result.json`

Baseline failure is stored at `evidence/baseline-failure.log`.
