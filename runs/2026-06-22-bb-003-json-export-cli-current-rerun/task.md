# BB-003 — JSON export for an existing CLI

## Objective
Add a `--json` option to the existing `logstats` Python CLI.

The default text output must remain unchanged. When `--json` is provided, the CLI must write machine-readable JSON to stdout with this exact shape:

```json
{
  "total_requests": 7,
  "status_counts": {"200": 4, "404": 2, "500": 1},
  "top_paths": [
    {"path": "/", "count": 3},
    {"path": "/api/items", "count": 2},
    {"path": "/login", "count": 1},
    {"path": "/missing", "count": 1}
  ]
}
```

## Constraints
- Make a minimal change to the existing package.
- Preserve default text output exactly.
- `status_counts` keys must be strings sorted by status code in JSON output.
- `top_paths` must be sorted by count descending, then path ascending for ties.
- Do not replace the project wholesale.

## Verification
From the fixture root:

```bash
python -m venv .venv
. .venv/bin/activate
pip install -q -e . pytest
pytest -q
python -m bb003_logstats --json sample.log
```
