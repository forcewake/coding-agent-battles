# BB-008 — Monorepo dependency upgrade metrics

## Scope

- Type: Tooling / monorepo
- Difficulty: L3
- Pass count: 6/6
- Token/cost extraction: ccusage-first where available, then direct CLI/SQLite fallback with exact per-run attribution.

## Agent metrics

| Agent | Verdict | Wall | Tokens | Normalized public cost | Telemetry source | Notes |
|---|---:|---:|---:|---:|---|---|
| OpenCode | PASS | 42.590s | 86,204 | $0.035012 | ccusage_opencode_exact_directory_session | Telemetry exact; independent verify passed |
| Claude | PASS | 34.085s | 124,808 | $0.060092 | claude_json_usage_normalized_public_cost | Telemetry exact; independent verify passed |
| MiMo | PASS | 42.267s | 187,931 | $0.055319 | mimocode_sqlite_session_exact_directory_normalized_public_cost | Telemetry exact; independent verify passed |
| Pi | PASS | 54.993s | 22,078 | $0.011694 | ccusage_pi_exact_project_path_normalized_public_cost | Telemetry exact; independent verify passed |
| Codex | PASS | 82.653s | 233,649 | $0.356317 | ccusage_codex_session_exact_log_session_id | Telemetry exact; independent verify passed |
| agy | PASS | 34.446s | n/a | n/a | unavailable | Telemetry unavailable |
