# Micro-RDD — D3 multipage cleanup

Topology: linear

## User request
Move Agent profiles off the home page, remove Latest scenario detail from home, create one detail page per scenario, make the UI cleaner/prettier, use D3.js for charts, and run `agy` with `Gemini 3.1 Pro (High)`.

## Scope
- Static GitHub Pages under `docs/`.
- Home: executive aggregate overview only.
- `agents.html`: aggregate agent profiles.
- `scenarios/<slug>.html`: per-scenario detail pages.
- D3 charts with local/vendor deterministic delivery if feasible.

## Non-goals
- Do not rerun benchmarks.
- Do not change benchmark truth values.
- Do not remove raw evidence/methodology links.

## Verification plan
- `python -m json.tool docs/site-data.json`
- HTML parser over all `docs/**/*.html`
- `node --check docs/*.js docs/**/*.js`
- local HTTP smoke for `/`, `/agents.html`, `/scenarios/bb-001.html`, `/scenarios/bb-003.html`
- browser console + visual QA public after deploy
- secret scan

## Implementation evidence
- `agy` implementation lane launched with `--model="Gemini 3.1 Pro (High)" --print-timeout 20m`.
- `/tmp/agy-gemini-d3-ui-refactor.log` contains `model="Gemini 3.1 Pro (High)"` and repeated selected-model override entries.
- Created `docs/agents.html`, `docs/scenarios/bb-001.html`, `docs/scenarios/bb-003.html`, and vendored `docs/vendor/d3.v7.min.js`.
- Home page no longer contains the Agent Profiles table or Latest Scenario Detail.
- `site-data.json` truth values preserved; only `slug` fields added for scenario routing.

## Verification completed
- JSON parse: `docs/site-data.json`.
- HTML parser: `docs/index.html`, `docs/agents.html`, `docs/scenarios/*.html`.
- JS syntax: `node --check docs/app.js`.
- Local HTTP smoke: `/`, `/agents.html`, `/scenarios/bb-001.html`, `/scenarios/bb-003.html`, `/vendor/d3.v7.min.js`.
- Browser console: zero JS errors on home, agents, and scenario page.
- Visual QA: home cleaner; D3 charts render; clipped agy label fixed; agents page and BB-003 detail page have no blocker issues.
- Secret scan: no hits in docs/RDD artifact.
