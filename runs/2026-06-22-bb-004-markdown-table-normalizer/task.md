# BB-004 — Markdown table normalizer

Implement a deterministic Markdown table normalizer.

## Requirements
- Normalize pipe tables into padded columns.
- Preserve non-table text.
- Output must be idempotent: `normalize(normalize(x)) == normalize(x)`.
- Separator row must be normalized to `---` per column.
- `python verify.py` must pass.
