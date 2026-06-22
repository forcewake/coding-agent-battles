# BB-009 — Observability instrumentation metrics

## Scope

- Type: Non-functional backend
- Difficulty: L3
- Pass count: 5/6
- Token/cost extraction: ccusage-first where available, then direct CLI/SQLite fallback with exact per-run attribution.

## Agent metrics

| Agent | Verdict | Wall | Tokens | Normalized public cost | Telemetry source | Notes |
|---|---:|---:|---:|---:|---|---|
| OpenCode | PASS | 58.357s | 87,637 | $0.030313 | ccusage_opencode_exact_directory_session | Telemetry exact; independent verify passed |
| Claude | PASS | 89.627s | 153,562 | $0.052263 | claude_json_usage_normalized_public_cost | Telemetry exact; independent verify passed |
| MiMo | PASS | 91.989s | 283,029 | $0.097538 | mimocode_sqlite_session_exact_directory_normalized_public_cost | Telemetry exact; independent verify passed |
| Pi | PASS | 68.880s | 19,534 | $0.013878 | ccusage_pi_exact_project_path_normalized_public_cost | Telemetry exact; independent verify passed |
| Codex | PASS | 100.717s | 197,851 | $0.438998 | ccusage_codex_session_exact_log_session_id | Telemetry exact; independent verify passed |
| agy | FAIL | 43.784s | n/a | n/a | unavailable | Telemetry unavailable |
