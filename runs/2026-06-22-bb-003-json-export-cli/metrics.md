# BB-003 Metrics — JSON export for existing CLI

Date: 2026-06-22

## Summary
BB-003 adds a `--json` export mode to an existing Python CLI while preserving default text output. Baseline was red in the intended way: default text passed, JSON flag failed with `unrecognized arguments: --json`.

## Scoreboard
| Agent | Exit | Wall-clock | Tokens | Public cost est. | Patch | Process | Verdict |
|---|---:|---:|---:|---:|---:|---:|---|
| OpenCode / GLM-5.2 | 0 | 66.732s | 149488 | $0.051295 | 100 | 86 | PASS |
| Claude Code / GLM-5.2 | 0 | 52.901s | 156994 | $0.072912 | 100 | 90 | PASS |
| MiMoCode / GLM-5.2 | 0 | 94.151s | 330730 | $0.108728 | 100 | 90 | PASS |
| Pi Coding Agent / GLM-5.2 | 0 | 56.314s | 5512 | $0.002751 | 100 | 90 | PASS |
| Codex CLI / GPT-5.5 | 0 | 104.966s | 242829 | $1.430545 | 100 | 100 | PASS |
| Antigravity agy / Gemini 3.5 Flash Medium | 0 | 147.780s | n/a | n/a | 100 | 90 | PASS |

## Independent verification
Hermes reran, for every final workspace:

```bash
python -m venv .venv
.venv/bin/python -m pip install -q -e . pytest
.venv/bin/python -m pytest -q
.venv/bin/python -m bb003_logstats --json sample.log
```

Every workspace produced valid JSON exactly matching the expected payload.

## Evidence
- Shared prompt: `evidence/prompt.txt`
- Baseline failure: `evidence/baseline-failure.log`
- Per-agent artifacts: `agents/<agent>/agent.log`, `diff.patch`, `git-status.txt`, `verify.log`
- Machine metrics: `metrics.json`

## Telemetry caveat
Token/cost was extracted where reliable local telemetry was available: OpenCode/MiMo SQLite, Claude JSON, Pi JSONL, Codex JSONL. agy still exposes process logs but no reliable token export.
