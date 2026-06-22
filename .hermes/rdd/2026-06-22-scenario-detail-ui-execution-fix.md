# Micro-RDD — Scenario detail UI and execution-score fix

Topology: linear

## User report
- Results / Metrics / JSON were raw file links.
- Latency-vs-token chart wasted card space and was hard to read.
- `Process quality 0–100 rubric` was flat for most agents and looked fake.

## Changes
- Replaced raw artifact CTAs with in-page tab buttons and an embedded artifact viewer; raw file remains secondary via `Open raw ↗`.
- Enlarged scatter plot, added gridlines, larger tick labels, wider label gutter, and responsive heights.
- Replaced placeholder `process` semantics with bounded `Execution quality 0–100 composite`.
- Recomputed all 12 scenarios; every scenario now has non-flat execution scores.
- Regenerated all 12 scenario pages from one common shell.

## Verification
- `node --check docs/app.js` passed.
- `python -m py_compile` for generator/extraction/scoring scripts passed.
- JSON validation passed.
- HTML parser checked index, agents, and all scenario pages.
- Browser headless DOM assertions passed for BB-001 through BB-012.
- BB-005 live browser interaction verified Results/Metrics/JSON switch in-page.
- Browser console for BB-005 had 0 JS errors.
