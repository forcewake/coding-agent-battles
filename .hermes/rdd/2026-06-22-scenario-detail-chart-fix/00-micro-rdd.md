# Micro-RDD — Scenario detail chart QA/fix

Topology: micro

## Scope
User reported visual/display bugs on scenario detail pages, especially `Process quality 0–100 rubric` and `Normalized public cost USD estimate` panels.

## Evidence
- Data inspection shows BB-002 and BB-004 through BB-012 have verified pass/fail and wall-clock results, but zero reliable token/cost datapoints for this bulk run.
- The shared renderer still drew token scatter axes with fake 0–1 domains and left the normalized-cost panel visually empty.
- Most new scenarios have identical process score values, which made the process rubric look suspicious without a tie explanation.

## Decision
- Treat missing telemetry as first-class state, not as a chart with fake axes.
- Keep wall-clock/process panels visible because those values are verified.
- Add explicit empty states for token/cost telemetry and a tie note when all process values are identical.

## Files changed
- `docs/app.js`
- `docs/styles.css`

## Verification plan
- JS syntax: `node --check docs/app.js`
- JSON/HTML syntax checks.
- Local HTTP route checks for all scenario pages.
- Browser/DOM QA for all 12 scenario pages.
- Public Pages deploy and public route/browser verification.

## Verification evidence
- `node --check docs/app.js` passed.
- `python -m json.tool docs/site-data.json` passed.
- HTML parser passed for home, agents, and all scenario pages.
- Local route smoke passed for BB-001 through BB-012.
- Chrome headless rendered-DOM assertions passed for all 12 scenario pages:
  - BB-001 and BB-003 keep real token/cost charts.
  - BB-002 and BB-004 through BB-012 show explicit token/cost telemetry empty states.
  - Identical-process scenarios show a tie note instead of implying a hidden winner.
- Browser visual QA passed for BB-012 (the user screenshot case) and BB-003 (telemetry-bearing regression case).
- Browser console was clean on both checked pages.
- Docs secret scan passed with the existing synthetic benchmark bearer-token allowlist.
