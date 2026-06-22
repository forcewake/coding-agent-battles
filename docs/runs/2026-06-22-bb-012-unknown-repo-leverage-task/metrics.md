# BB-012 — Unknown repo leverage task metrics

## Scope

- Type: External helper leverage
- Difficulty: L4
- Pass count: 6/6
- Token/cost extraction: ccusage-first where available, then direct CLI/SQLite fallback with exact per-run attribution.

## Agent metrics

| Agent | Verdict | Wall | Tokens | Normalized public cost | Telemetry source | Notes |
|---|---:|---:|---:|---:|---|---|
| OpenCode | PASS | 52.259s | 55,799 | $0.023785 | ccusage_opencode_exact_directory_session | Telemetry exact; independent verify passed |
| Claude | PASS | 43.710s | 126,638 | $0.042389 | claude_json_usage_normalized_public_cost | Telemetry exact; independent verify passed |
| MiMo | PASS | 64.967s | 213,715 | $0.065665 | mimocode_sqlite_session_exact_directory_normalized_public_cost | Telemetry exact; independent verify passed |
| Pi | PASS | 86.329s | 38,848 | $0.015392 | ccusage_pi_exact_project_path_normalized_public_cost | Telemetry exact; independent verify passed |
| Codex | PASS | 90.124s | 167,667 | $0.424154 | ccusage_codex_session_exact_log_session_id | Telemetry exact; independent verify passed |
| agy | PASS | 102.463s | n/a | n/a | unavailable | Telemetry unavailable |
