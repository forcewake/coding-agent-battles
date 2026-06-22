# BB-007 — SQLite migration with rollback metrics

## Scope

- Type: Data migration
- Difficulty: L2
- Pass count: 6/6
- Token/cost extraction: ccusage-first where available, then direct CLI/SQLite fallback with exact per-run attribution.

## Agent metrics

| Agent | Verdict | Wall | Tokens | Normalized public cost | Telemetry source | Notes |
|---|---:|---:|---:|---:|---|---|
| OpenCode | PASS | 48.124s | 64,976 | $0.026777 | ccusage_opencode_exact_directory_session | Telemetry exact; independent verify passed |
| Claude | PASS | 86.768s | 183,359 | $0.088476 | claude_json_usage_normalized_public_cost | Telemetry exact; independent verify passed |
| MiMo | PASS | 82.405s | 191,087 | $0.059777 | mimocode_sqlite_session_exact_directory_normalized_public_cost | Telemetry exact; independent verify passed |
| Pi | PASS | 137.179s | 40,117 | $0.025923 | ccusage_pi_exact_project_path_normalized_public_cost | Telemetry exact; independent verify passed |
| Codex | PASS | 122.860s | 176,231 | $0.418060 | ccusage_codex_session_exact_log_session_id | Telemetry exact; independent verify passed |
| agy | PASS | 74.759s | n/a | n/a | unavailable | Telemetry unavailable |
