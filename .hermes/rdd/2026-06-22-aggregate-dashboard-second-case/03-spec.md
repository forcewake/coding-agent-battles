# Spec: Home aggregate dashboard + BB-003 second case

## Orchestration Note
Degraded-controller mode due delegate model routing failure before phase execution.

## Overview
Add a second benchmark run (`BB-003 JSON export to existing CLI`) and update GitHub Pages to show aggregate multi-scenario results across BB-001 and BB-003.

## Functional Requirements
- FR-1: Add `tasks/BB-003-json-export-cli/` with task spec, fixture package, sample log, tests, and broken baseline.
- FR-2: Run BB-003 through six agents: mimo, opencode, agy, claude-code, codex-cli, pi.
- FR-3: Store raw artifacts under `runs/2026-06-22-bb-003-json-export-cli/` including prompt, harness, logs, diffs, verify logs, results, metrics JSON/MD.
- FR-4: Update `docs/site-data.json` to include both scenario summaries and aggregate agent profiles.
- FR-5: Update Pages UI to present a home aggregate dashboard: KPI strip, scenario matrix, scenario cards, agent profiles, and keep raw evidence links.
- FR-6: Preserve normalized public cost semantics; if token extraction is unavailable for BB-003, mark unavailable/estimated rather than inventing.

## Non-Functional Requirements
- NFR-1: No secrets or provider local auth files committed.
- NFR-2: Static Pages only; no new build chain.
- NFR-3: Dashboard must be browser-verifiable and readable at desktop width.

## Acceptance Criteria
- [ ] AC-1: BB-003 baseline fails before agent changes.
- [ ] AC-2: At least one full six-agent BB-003 run is captured with per-agent logs/diffs/meta.
- [ ] AC-3: Hermes verification passes for every successful BB-003 agent workspace and records pytest + JSON CLI smoke.
- [ ] AC-4: `docs/site-data.json` validates and contains at least two scenarios.
- [ ] AC-5: Pages local and public checks show an aggregate home view with Agent × Scenario matrix.
- [ ] AC-6: Browser console has zero JS errors on deployed Pages.

## Out of Scope
- Multi-page routing and historical filters beyond the first two scenarios.
- Perfect token extraction for every agent on BB-003.
- Running expensive UI/backend tasks in this iteration.
