# BB-010 — DOCX extraction quality fix results

Improve OOXML/DOCX extraction to preserve paragraph/table order and XML entity decoding.

## Verification summary

| Agent | Verdict | Wall | Agent exit | Verify exit | Patch | Execution |
|---|---:|---:|---:|---:|---:|---:|
| OpenCode | PASS | 67.775s | 0 | 0 | 100 | 97 |
| Claude | PASS | 69.886s | 0 | 0 | 100 | 92 |
| MiMo | PASS | 336.866s | 0 | 0 | 100 | 74 |
| Pi | PASS | 79.757s | 0 | 0 | 100 | 99 |
| Codex | PASS | 129.014s | 0 | 0 | 100 | 82 |
| agy | PASS | 103.864s | 0 | 0 | 100 | 82 |

## Evidence

Each agent has committed-style artifacts under `agents/<agent>/`:

- `agent.log`
- `agent-meta.txt`
- `diff.patch`
- `git-status.txt`
- `verify.log`
- `result.json`

Baseline failure is stored at `evidence/baseline-failure.log`.
