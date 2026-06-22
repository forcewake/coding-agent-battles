# BB-008 — Monorepo dependency upgrade

A shared utility changed its API from `slugify(text)` to `makeSlug(text, options)`. Fix the app package without breaking compatibility tests.

## Requirements
- Update app code to use the new shared API.
- Preserve stable slugs: lowercase, trim, collapse non-alphanumerics to single dash.
- Do not reintroduce the old `slugify` export.
- `python verify.py` must pass.
