# Coding Agent Battles — claim ledger audit

- Generated: `2026-06-22T21:12:45.658164+00:00`
- Commit observed during generation: `bfdf7c6ef4ab5fc85adf4bd42ece3245c7b0b6d4`
- Commit note: This is the source revision observed when the audit files were generated. A commit that contains regenerated audit files necessarily has a different SHA; compare non-audit files for data changes.
- Overall: **PASS_WITH_WARNINGS**
- Counts: `{'PASS': 824, 'WARN': 12, 'FAIL': 0}`
- Non-pass severities: `{'blocker': 0, 'major': 0, 'minor': 12, 'info': 0}`

## Failed / warning checks

| Status | Severity | ID | Claim | Evidence | Details |
|---|---|---|---|---|---|
| WARN | minor | `BB-001.opencode.telemetry_breakdown_total` | BB-001/opencode telemetry has exact provenance but token breakdown does not sum exactly to total | `docs/site-data.json`<br>`docs/runs/2026-06-22-bb-001-broken-cli-argument-current-rerun/metrics.json` | strategy=ccusage_opencode_exact_directory_session source=ccusage opencode session + opencode.log exact directory/session id token_total_candidates=[195562, 195562] tokens=195887 |
| WARN | minor | `BB-002.opencode.telemetry_breakdown_total` | BB-002/opencode telemetry has exact provenance but token breakdown does not sum exactly to total | `docs/site-data.json`<br>`docs/runs/2026-06-22-bb-002-csv-edge-case-parser/metrics.json` | strategy=ccusage_opencode_exact_directory_session source=ccusage opencode session + opencode.log exact directory/session id token_total_candidates=[105836, 105836] tokens=105968 |
| WARN | minor | `BB-003.opencode.telemetry_breakdown_total` | BB-003/opencode telemetry has exact provenance but token breakdown does not sum exactly to total | `docs/site-data.json`<br>`docs/runs/2026-06-22-bb-003-json-export-cli-current-rerun/metrics.json` | strategy=ccusage_opencode_exact_directory_session source=ccusage opencode session + opencode.log exact directory/session id token_total_candidates=[149244, 149244] tokens=149410 |
| WARN | minor | `BB-004.opencode.telemetry_breakdown_total` | BB-004/opencode telemetry has exact provenance but token breakdown does not sum exactly to total | `docs/site-data.json`<br>`docs/runs/2026-06-22-bb-004-markdown-table-normalizer/metrics.json` | strategy=ccusage_opencode_exact_directory_session source=ccusage opencode session + opencode.log exact directory/session id token_total_candidates=[98429, 98429] tokens=103515 |
| WARN | minor | `BB-005.opencode.telemetry_breakdown_total` | BB-005/opencode telemetry has exact provenance but token breakdown does not sum exactly to total | `docs/site-data.json`<br>`docs/runs/2026-06-22-bb-005-fastapi-auth-middleware-bug/metrics.json` | strategy=ccusage_opencode_exact_directory_session source=ccusage opencode session + opencode.log exact directory/session id token_total_candidates=[53541, 53541] tokens=53635 |
| WARN | minor | `BB-006.opencode.telemetry_breakdown_total` | BB-006/opencode telemetry has exact provenance but token breakdown does not sum exactly to total | `docs/site-data.json`<br>`docs/runs/2026-06-22-bb-006-react-filter-search-ui/metrics.json` | strategy=ccusage_opencode_exact_directory_session source=ccusage opencode session + opencode.log exact directory/session id token_total_candidates=[51606, 51606] tokens=51697 |
| WARN | minor | `BB-007.opencode.telemetry_breakdown_total` | BB-007/opencode telemetry has exact provenance but token breakdown does not sum exactly to total | `docs/site-data.json`<br>`docs/runs/2026-06-22-bb-007-sqlite-migration-rollback/metrics.json` | strategy=ccusage_opencode_exact_directory_session source=ccusage opencode session + opencode.log exact directory/session id token_total_candidates=[64446, 64446] tokens=64976 |
| WARN | minor | `BB-008.opencode.telemetry_breakdown_total` | BB-008/opencode telemetry has exact provenance but token breakdown does not sum exactly to total | `docs/site-data.json`<br>`docs/runs/2026-06-22-bb-008-monorepo-dependency-upgrade/metrics.json` | strategy=ccusage_opencode_exact_directory_session source=ccusage opencode session + opencode.log exact directory/session id token_total_candidates=[86179, 86179] tokens=86204 |
| WARN | minor | `BB-009.opencode.telemetry_breakdown_total` | BB-009/opencode telemetry has exact provenance but token breakdown does not sum exactly to total | `docs/site-data.json`<br>`docs/runs/2026-06-22-bb-009-observability-instrumentation/metrics.json` | strategy=ccusage_opencode_exact_directory_session source=ccusage opencode session + opencode.log exact directory/session id token_total_candidates=[87452, 87452] tokens=87637 |
| WARN | minor | `BB-010.opencode.telemetry_breakdown_total` | BB-010/opencode telemetry has exact provenance but token breakdown does not sum exactly to total | `docs/site-data.json`<br>`docs/runs/2026-06-22-bb-010-docx-extraction-quality-fix/metrics.json` | strategy=ccusage_opencode_exact_directory_session source=ccusage opencode session + opencode.log exact directory/session id token_total_candidates=[80350, 80350] tokens=81296 |
| WARN | minor | `BB-011.opencode.telemetry_breakdown_total` | BB-011/opencode telemetry has exact provenance but token breakdown does not sum exactly to total | `docs/site-data.json`<br>`docs/runs/2026-06-22-bb-011-greenfield-mini-product/metrics.json` | strategy=ccusage_opencode_exact_directory_session source=ccusage opencode session + opencode.log exact directory/session id token_total_candidates=[53020, 53020] tokens=53112 |
| WARN | minor | `BB-012.opencode.telemetry_breakdown_total` | BB-012/opencode telemetry has exact provenance but token breakdown does not sum exactly to total | `docs/site-data.json`<br>`docs/runs/2026-06-22-bb-012-unknown-repo-leverage-task/metrics.json` | strategy=ccusage_opencode_exact_directory_session source=ccusage opencode session + opencode.log exact directory/session id token_total_candidates=[55344, 55344] tokens=55799 |

## Audit scope

This deterministic pass checks committed/public dashboard claims against committed run artifacts:

- `docs/site-data.json`
- `docs/runs/**/{metrics.json,metrics.md,results.md}`
- `runs/**/{metrics.json,results.md,agents/*/result.json,agents/*/verify.log}`
- optional public rendered scenario pages when `--public` is used

The ledger intentionally does not infer correctness from private provider databases or uncommitted logs; those are only referenced through already-published telemetry provenance fields.
