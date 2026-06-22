# Telemetry provenance manifest

This file exists because token/cost evidence must not be implied to be fully raw-replayable from public files when the source was a local provider store or `ccusage` database.

## Counts by evidence level

| Evidence level | Rows |
|---|---:|
| `committed_raw_agent_json` | 10 |
| `committed_session_id_plus_local_ccusage_extract` | 10 |
| `legacy_published_metric_without_row_level_provenance` | 10 |
| `local_ccusage_project_path_extract_not_raw_committed` | 10 |
| `local_mimocode_sqlite_extract_not_raw_committed` | 10 |
| `local_opencode_log_plus_ccusage_extract_not_raw_committed` | 10 |
| `unavailable` | 12 |

## Limitations

- Some token/cost rows are exact local attributions from ccusage or provider stores whose raw databases/logs are intentionally not committed because they can contain private paths/session data.
- Rows marked *_not_raw_committed are auditable as sanitized extracted metrics plus run/session attribution, not as raw-provider replay artifacts.
- BB-001 and BB-003 are legacy early runs with published token/cost values but without row-level telemetry provenance fields.
- agy/Antigravity token and cost telemetry remains unavailable where no reliable export exists.

## Machine-readable manifest

See `docs/audit/telemetry-provenance.json`.
