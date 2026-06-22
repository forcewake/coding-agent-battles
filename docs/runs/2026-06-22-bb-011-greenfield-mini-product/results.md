# BB-011 — Greenfield mini-product results

Build a tiny FastAPI benchmark registry from tests/spec.

## Verification summary

| Agent | Verdict | Wall | Agent exit | Verify exit | Patch | Execution |
|---|---:|---:|---:|---:|---:|---:|
| OpenCode | PASS | 47.141s | 0 | 0 | 100 | 100 |
| Claude | PASS | 95.167s | 0 | 0 | 100 | 91 |
| MiMo | PASS | 49.366s | 0 | 0 | 100 | 100 |
| Pi | PASS | 71.199s | 0 | 0 | 100 | 96 |
| Codex | PASS | 101.535s | 0 | 0 | 100 | 90 |
| agy | PASS | 50.500s | 0 | 0 | 100 | 99 |

## Evidence

Each agent has committed-style artifacts under `agents/<agent>/`:

- `agent.log`
- `agent-meta.txt`
- `diff.patch`
- `git-status.txt`
- `verify.log`
- `result.json`

Baseline failure is stored at `evidence/baseline-failure.log`.
