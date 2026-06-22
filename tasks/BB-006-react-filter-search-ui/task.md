# BB-006 — React filter/search UI

Fix the browser-visible search/filter state model. The UI is represented by a small dependency-free module to keep the benchmark reproducible.

## Requirements
- `filterItems(items, query, tag)` must be case-insensitive.
- Query searches title and description.
- Tag `all` disables tag filtering.
- Result order is stable by original input order.
- Empty result state text must be `No matching agents`.
- `python verify.py` must pass.
