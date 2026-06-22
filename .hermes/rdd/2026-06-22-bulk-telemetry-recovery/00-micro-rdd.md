# Micro-RDD — Bulk telemetry recovery

## Trigger
User challenged why token/cost data was missing from bulk scenario pages despite raw data existing.

## Root cause
`scripts/update_dashboard_from_remaining_suite.py` hardcoded bulk run agents with `tokens: None` and `cost: None`, and emitted metrics markdown saying telemetry was not normalized yet. Raw sources contained enough reliable per-run telemetry for 5/6 agents.

## Fix
Added `scripts/extract_bulk_telemetry.py` and wired it into the dashboard updater.

Exact attribution sources:
- Claude: per-run `agents/claude-code/agent-output.json` usage + normalized GLM pricing.
- Codex: `ccusage codex session` matched by `agent.log` session id.
- OpenCode: `ccusage opencode session` matched by `~/.local/share/opencode/log/opencode.log` exact directory/session id.
- MiMo: `~/.local/share/mimocode/mimocode.db` exact `session.directory` + message token usage.
- Pi: `ccusage pi session` exact `projectPath`, with normalized public ZAI cost recalculated because native `totalCost` is 0.
- agy: remains unavailable; Antigravity transcript still lacks reliable token/cost export.

## Verification
- Restored telemetry for 50 bulk agent runs.
- Every scenario now has 5/6 known token/cost telemetry.
- `node --check docs/app.js` passed.
- `python -m py_compile scripts/extract_bulk_telemetry.py scripts/update_dashboard_from_remaining_suite.py` passed.
- `python -m json.tool docs/site-data.json` passed.
- Chrome rendered-DOM assertions passed for BB-001..BB-012: cost bars exist, token scatter exists, no telemetry-empty state remains except agy lane.
- Browser visual QA on BB-012 confirmed five token/cost agents and agy n/a.
