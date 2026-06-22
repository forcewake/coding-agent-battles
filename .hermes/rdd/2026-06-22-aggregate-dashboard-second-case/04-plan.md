# Plan: Home aggregate dashboard + BB-003 second case

> **For Hermes:** Degraded-controller mode. Execute directly with strong verification because delegate_task failed before work due model routing.

## Task 1: Materialize BB-003 fixture
Create task spec, Python package, sample log, default text CLI, tests including failing `--json` behavior. Verify baseline red.

## Task 2: Prepare isolated run
Create `runs/2026-06-22-bb-003-json-export-cli`, copy fixture to six workspaces, initialize git baseline in each, write shared prompt and harness.

## Task 3: Run six agents
Launch tracked background processes for mimo, opencode, agy, claude-code, codex-cli, pi. Capture logs/meta.

## Task 4: Verify and score
Run fresh Hermes verification for each workspace. Save diffs, statuses, verify logs. Create results.md, metrics.json, metrics.md.

## Task 5: Generate aggregate dashboard data
Read BB-001 and BB-003 metrics, compute scenario summaries, agent aggregate profiles, matrix rows, and latest run detail data into `docs/site-data.json`.

## Task 6: Update Pages UI
Refactor `docs/index.html`, `docs/app.js`, `docs/styles.css` for aggregate home while preserving run detail charts/evidence.

## Task 7: Verification and deploy
Run JSON/HTML validation, secret scan, local HTTP/browser QA, commit/push, watch Pages workflow, public curl and browser QA.
