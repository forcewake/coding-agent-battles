# BB-004 — Markdown table normalizer metrics

## Scope

- Type: Text processing
- Difficulty: L1
- Pass count: 6/6
- Token/cost extraction: ccusage-first where available, then direct CLI/SQLite fallback with exact per-run attribution.

## Agent metrics

| Agent | Verdict | Wall | Tokens | Normalized public cost | Telemetry source | Notes |
|---|---:|---:|---:|---:|---|---|
| OpenCode | PASS | 167.030s | 103,515 | $0.062082 | ccusage_opencode_exact_directory_session | Telemetry exact; independent verify passed |
| Claude | PASS | 169.013s | 169,366 | $0.085769 | claude_json_usage_normalized_public_cost | Telemetry exact; independent verify passed |
| MiMo | PASS | 190.220s | 227,270 | $0.094997 | mimocode_sqlite_session_exact_directory_normalized_public_cost | Telemetry exact; independent verify passed |
| Pi | PASS | 247.114s | 62,200 | $0.059673 | ccusage_pi_exact_project_path_normalized_public_cost | Telemetry exact; independent verify passed |
| Codex | PASS | 219.382s | 327,859 | $0.757551 | ccusage_codex_session_exact_log_session_id | Telemetry exact; independent verify passed |
| agy | PASS | 113.300s | n/a | n/a | unavailable | Telemetry unavailable |
