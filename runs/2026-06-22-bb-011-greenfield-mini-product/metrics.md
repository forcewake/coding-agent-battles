# BB-011 — Greenfield mini-product metrics

## Scope

- Type: Greenfield product
- Difficulty: L4
- Pass count: 6/6
- Token/cost extraction: ccusage-first where available, then direct CLI/SQLite fallback with exact per-run attribution.

## Agent metrics

| Agent | Verdict | Wall | Tokens | Normalized public cost | Telemetry source | Notes |
|---|---:|---:|---:|---:|---|---|
| OpenCode | PASS | 47.141s | 53,112 | $0.020773 | ccusage_opencode_exact_directory_session | Telemetry exact; independent verify passed |
| Claude | PASS | 95.167s | 177,821 | $0.056421 | claude_json_usage_normalized_public_cost | Telemetry exact; independent verify passed |
| MiMo | PASS | 49.366s | 190,265 | $0.058130 | mimocode_sqlite_session_exact_directory_normalized_public_cost | Telemetry exact; independent verify passed |
| Pi | PASS | 71.199s | 30,285 | $0.012942 | ccusage_pi_exact_project_path_normalized_public_cost | Telemetry exact; independent verify passed |
| Codex | PASS | 101.535s | 204,368 | $0.400817 | ccusage_codex_session_exact_log_session_id | Telemetry exact; independent verify passed |
| agy | PASS | 50.500s | n/a | n/a | unavailable | Telemetry unavailable |
