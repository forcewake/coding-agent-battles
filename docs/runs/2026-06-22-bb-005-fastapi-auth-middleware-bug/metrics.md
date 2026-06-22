# BB-005 — FastAPI auth middleware bug metrics

## Scope

- Type: Backend debugging
- Difficulty: L2
- Pass count: 5/6
- Token/cost extraction: ccusage-first where available, then direct CLI/SQLite fallback with exact per-run attribution.

## Agent metrics

| Agent | Verdict | Wall | Tokens | Normalized public cost | Telemetry source | Notes |
|---|---:|---:|---:|---:|---|---|
| OpenCode | PASS | 43.633s | 53,635 | $0.023405 | ccusage_opencode_exact_directory_session | Telemetry exact; independent verify passed |
| Claude | PASS | 47.969s | 153,526 | $0.050461 | claude_json_usage_normalized_public_cost | Telemetry exact; independent verify passed |
| MiMo | PASS | 46.894s | 128,828 | $0.041709 | mimocode_sqlite_session_exact_directory_normalized_public_cost | Telemetry exact; independent verify passed |
| Pi | PASS | 87.805s | 34,046 | $0.017220 | ccusage_pi_exact_project_path_normalized_public_cost | Telemetry exact; independent verify passed |
| Codex | PASS | 100.380s | 252,306 | $0.400477 | ccusage_codex_session_exact_log_session_id | Telemetry exact; independent verify passed |
| agy | FAIL | 47.220s | n/a | n/a | unavailable | Telemetry unavailable |
