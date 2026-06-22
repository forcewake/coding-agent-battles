# Coding Agent Battles — cross-check summary

## Verdict after current reruns

- Deterministic audit: **PASS_WITH_WARNINGS**
- Deterministic failures: **0**
- Blockers: **0**
- Major warnings: **0**
- Remaining warnings: **12 minor OpenCode accounting notes**

## What changed in this closure pass

1. **BB-001 and BB-003 were rerun with the current harness** for all six agents.
   - New run IDs:
     - `2026-06-22-bb-001-broken-cli-argument-current-rerun`
     - `2026-06-22-bb-003-json-export-cli-current-rerun`
   - Each now has per-agent `result.json`, `verify.log`, `agent.log`, `diff.patch`, `metrics.json`, `metrics.md`, and `results.md`.
   - Both reruns are **6/6 PASS**.
2. Added deterministic `verify.py` files to the BB-001 and BB-003 fixtures so they can be replayed through the same harness as BB-002 and BB-004–BB-012.
3. Removed stale public/raw legacy BB-001 and BB-003 run directories that conflicted with the authoritative current reruns.
4. Recovered token/cost telemetry for all non-agy rows, including BB-001 and BB-003 current reruns.
5. Added sanitized row-level telemetry exports under `docs/audit/sanitized-telemetry/`.
6. Rebuilt telemetry provenance, execution scores, site data, public run mirrors, and claim ledger.

## Current deterministic counts

```json
{
  "PASS": 824,
  "WARN": 12,
  "FAIL": 0
}
```

## Telemetry status

| Category | Rows | Status |
|---|---:|---|
| OpenCode | 12 | exact ccusage/opencode directory attribution; minor provider-accounting total-vs-breakdown warnings |
| Claude Code | 12 | committed raw `agent-output.json` usage |
| MiMo | 12 | local MiMoCode SQLite exact directory/session extraction, sanitized export published |
| Pi | 12 | ccusage exact projectPath extraction, sanitized export published |
| Codex CLI | 12 | ccusage exact session-id extraction, sanitized export published |
| agy | 12 | unavailable; `ccusage gemini` returned 0 sessions and `tokscale antigravity status` reports 0 cached sessions |

## Remaining accepted notes

| Severity | Issue | Decision |
|---|---|---|
| Minor | OpenCode token breakdown does not exactly sum to ccusage total | Documented provider-accounting nuance; total/cost use ccusage reported total. |
| Minor | agy token/cost telemetry unavailable | Explicitly marked unavailable for all 12 agy rows after focused `ccusage gemini` and `tokscale antigravity` probes. |
| Minor | Sanitized telemetry exports are not raw provider DB/log dumps | Intentional: local provider stores are not committed; row-level sanitized records expose extracted metrics and attribution without private paths. |

## Artifacts

- `docs/audit/claim-ledger.json`
- `docs/audit/claim-ledger.md`
- `docs/audit/telemetry-provenance.json`
- `docs/audit/telemetry-provenance.md`
- `docs/audit/sanitized-telemetry/index.json`
- `docs/audit/sanitized-telemetry/all-records.json`
- `docs/audit/llm-review-prompt.md`

## Interpretation boundary

The benchmark remains a **scaffold + configured model** comparison, not a scaffold-only leaderboard. It is now uniform across all 12 scenarios for verdict/wall/diff/verification artifacts; token/cost is complete for 5/6 agents and explicitly unavailable for agy.
