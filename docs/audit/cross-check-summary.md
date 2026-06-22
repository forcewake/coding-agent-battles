# Coding Agent Battles — cross-check summary

## Verdict

- Deterministic audit: **PASS_WITH_WARNINGS**
- Gemini 3.1 Pro High adversarial review: **APPROVE_WITH_NOTES**
- Blockers: **0**
- Deterministic failures: **0**

## What was fixed during cross-check

1. Codex normalized public cost now includes reasoning tokens as output tokens; `vendorCost` preserves native/ccusage value separately.
2. Execution quality no longer mixes token/cost telemetry into the score; efficiency remains visible in separate token/cost panels.
3. Public wording no longer claims every number is raw-backed by committed logs; telemetry caveats are explicit.
4. `docs/audit/telemetry-provenance.json` and `.md` publish evidence levels for all 72 rows.
5. BB-001 and BB-003 now show a visible legacy provenance warning on scenario pages.

## Remaining accepted notes

| Severity | Issue | Decision |
|---|---|---|
| Major | BB-001/BB-003 lack per-agent `result.json` | Accepted as legacy early-run artifact gap; visible scenario warning added. Rerun if strict uniform artifact schema is required. |
| Major | BB-001/BB-003 cost rows lack row-level telemetry provenance | Accepted as legacy published metrics; visible warning and manifest caveat added. Rerun if full provenance is required. |
| Minor | OpenCode token breakdown does not exactly sum to total | Documented provider-accounting nuance; total/cost use ccusage reported total. |
| Minor | Some telemetry is not raw-replayable from public files | Documented in telemetry provenance manifest; raw local provider stores are intentionally not committed. |

## Artifacts

- `docs/audit/claim-ledger.json`
- `docs/audit/claim-ledger.md`
- `docs/audit/telemetry-provenance.json`
- `docs/audit/telemetry-provenance.md`
- `docs/audit/llm-review-prompt.md`
- `docs/audit/gemini-3.1-pro-high-review-final2.json`

## Deterministic counts

```json
{
  "PASS": 788,
  "WARN": 32,
  "FAIL": 0
}
```

## Gemini final methodology notes

- Dashboard correctly claims 12 scenarios, 72 runs, 70 passes, and 2 fails (verified in site-data.json and raw runs).
- Fastest, cheapest, and best execution claims are correctly aggregated from the underlying wall-clock, cost, and process scores.
- Execution quality is fully transparent and explicitly excludes token/cost efficiency, which are evaluated separately.
- Normalized public cost is clearly separated from vendorCost throughout the dataset.
- The UI is careful not to overclaim, explicitly pointing users to the audit pack for provenance caveats instead of claiming fully raw-backed telemetry for all rows.
