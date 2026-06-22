# Micro-RDD — ccusage source correction

Topology: micro

## Scope
Correct benchmark telemetry methodology after user pointed out that ccusage supports more local coding-agent data sources than the repo narrative implied.

## Evidence gathered
- `npx --yes ccusage@latest --version` → `ccusage 20.0.14`.
- `ccusage <namespace> --help` confirmed focused namespaces for `claude`, `codex`, `opencode`, `hermes`, `pi`, and `gemini`.
- ccusage docs consulted:
  - https://ccusage.com/guide/claude/
  - https://ccusage.com/guide/codex/
  - https://ccusage.com/guide/opencode/
  - https://ccusage.com/guide/hermes/
  - https://ccusage.com/guide/pi/
  - https://ccusage.com/guide/gemini/
- Local smoke on 2026-06-22:
  - `ccusage pi session --json --since 2026-06-22 --until 2026-06-22` found 2 sessions and contains BB-001/BB-003 paths.
  - `ccusage codex session --json --since 2026-06-22 --until 2026-06-22` found 3 sessions and totals.
  - `ccusage opencode session --json --since 2026-06-22 --until 2026-06-22` found 3 sessions and totals.
  - `ccusage hermes session --json --since 2026-06-22 --until 2026-06-22` found 10 Hermes sessions.
  - `ccusage claude ...` and `ccusage gemini ...` returned zero sessions for these specific benchmark runs through default dirs.

## Decision
Use ccusage as the primary telemetry collector where it can map a benchmark run/session. Keep direct JSON/JSONL/SQLite extraction as fallback and cross-check, especially when:
- a run was launched with no persistent project/session logs;
- ccusage aggregates a day/source but does not expose the benchmark workspace path/session mapping needed for per-run attribution;
- the participant is Antigravity `agy`, whose local transcript is under `~/.gemini/antigravity-cli/...` and is not the same as ccusage Gemini CLI support under `~/.gemini/tmp/*/chats/`.

## Files changed
- `README.md`
- `docs/metrics.md`
- `docs/index.html`
- `docs/site-data.json`
- `runs/2026-06-22-bb-001-broken-cli-argument-telemetry-rerun/metrics.md`
- `runs/2026-06-22-bb-001-broken-cli-argument-telemetry-rerun/evidence/telemetry-extraction.md`
- `runs/2026-06-22-bb-003-json-export-cli/metrics.md`
- `runs/2026-06-22-bb-003-json-export-cli/results.md`
- `runs/2026-06-22-bb-003-json-export-cli/metrics.json`

## Verification plan
- JSON parse `docs/site-data.json` and BB-003 `metrics.json`.
- HTML parse `docs/index.html`.
- Grep docs for ccusage-supported source language.
- Run a lightweight secret scan.
