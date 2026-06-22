# BB-012 — Unknown repo leverage task

Use the provided `vendor/textkit` helper instead of reimplementing tokenization incorrectly.

## Requirements
- `summarize(text)` returns top words with counts, sorted by count desc then word asc.
- Use `vendor.textkit.words` so punctuation/case handling matches the vendor helper.
- Ignore stopwords from `vendor.textkit.STOPWORDS`.
- Return at most 3 entries as list of `{word,count}` dicts.
- `python verify.py` must pass.
