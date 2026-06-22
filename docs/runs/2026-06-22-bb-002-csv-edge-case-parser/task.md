# BB-002 — CSV edge-case parser

Fix the CSV summary library. The current parser uses naive `str.split(',')`, so quoted commas, escaped quotes, and blank rows are mishandled.

## Requirements
- Use proper CSV parsing semantics.
- Preserve the public API: `summarize_people_csv(text: str) -> dict`.
- Ignore fully blank rows.
- Count valid rows and group by city.
- Keep deterministic sorted city keys.
- `python verify.py` must pass.
