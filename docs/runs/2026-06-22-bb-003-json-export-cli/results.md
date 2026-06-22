# BB-003 Results — JSON export for existing CLI

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
`ccusage` supports the relevant focused sources (`claude`, `codex`, `opencode`, `hermes`, `pi`, `gemini`) and is now the preferred first-pass collector. For this specific BB-003 run:

- `ccusage pi session --json --since 2026-06-22 --until 2026-06-22` found the Pi session and benchmark path.
- `ccusage codex ...` and `ccusage opencode ...` found same-day source totals, but the committed per-run metrics keep direct Codex JSONL / OpenCode SQLite workspace-matched extraction for deterministic attribution.
- `ccusage claude ...` returned no default-dir sessions for this run because the harness used direct JSON output rather than persistent Claude project logs.
- `ccusage gemini ...` supports Gemini CLI logs, but Antigravity `agy` stores different transcripts and still exposes no reliable token/cost export here.

Therefore token/cost is recorded from the most attributable reliable source per agent, with ccusage as primary where it maps cleanly and fallback/cross-check extraction otherwise.
