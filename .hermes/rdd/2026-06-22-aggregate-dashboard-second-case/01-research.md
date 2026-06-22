# Research: Aggregate dashboard + second benchmark case

## Orchestration Note
The planned research subagent failed before doing work because the configured delegate model `claude-opus-4.7` is not supported through the current Codex/ChatGPT account. This artifact is written in degraded-controller mode and will be verified by local file/test/browser evidence.

## Problem Statement
The public GitHub Pages site currently visualizes one run (`BB-001`) well, but it does not yet show how the benchmark will look once multiple scenarios exist. The user asked for a home aggregate dashboard and one additional live case so the site demonstrates the real-life multi-scenario experience.

## Current Repo Findings
- `tasks/backlog.md` recommends BB-005 after BB-001, but also lists lower-risk feature tasks BB-002/BB-003 that are cheaper and deterministic for a second same-day run.
- Existing `runs/2026-06-22-bb-001-broken-cli-argument-telemetry-rerun/metrics.json` already has the machine-readable agent schema required for aggregation.
- Existing `docs/site-data.json` is single-run oriented: one `task`, one `agents` list, one `links` object.
- Existing `docs/index.html` is a polished detail page, not a corpus home page.
- Existing benchmark harness supports six agents and telemetry-oriented CLI invocations.

## Candidate Second Scenarios
### BB-005 FastAPI auth middleware bug
Pros: realistic backend debugging and HTTP smoke. Cons: needs dependency install and API runtime; more time/risk across six agents; higher chance of irrelevant framework churn.

### BB-006 React filter/search UI
Pros: browser-visible and ideal for visual dashboard proof. Cons: requires JS build/browser test harness and likely much longer agent runs.

### BB-003 JSON export to existing CLI — Recommended
Pros: deterministic Python CLI feature addition; bigger than BB-001; clear tests plus CLI smoke; all agents can solve in one run; produces meaningful contrast in process and diff size without making the demo too slow. Cons: still not a full backend/UI task.

## Aggregate Dashboard Data Model Recommendations
Add `docs/site-data.json` fields:
- `scenarios[]`: each scenario summary with id, type, difficulty, run id, status, best/fastest/cheapest/process winners, and raw links.
- `matrix[]` or derive Agent × Scenario from `scenarios[].agents`.
- `agents[]` aggregate profiles with runs, pass rate, median/average quality, process, wall-clock, tokens, normalized cost, telemetry coverage.
- Keep existing per-run detail data available for the latest run to avoid breaking the detail charts.

## GitHub Pages / Visualization Recommendations
The home should become a benchmark cockpit:
1. portfolio KPI strip: scenarios, agent runs, pass rate, normalized public cost;
2. Agent × Scenario heatmap;
3. Pareto/cost-quality frontier;
4. scenario cards with winners and evidence links;
5. agent profile strip showing pass rate, median process, cost/pass, and telemetry coverage.

## Verification Recommendations
- Baseline for BB-003 must fail before agents run.
- Each agent must run in an isolated workspace from the same fixture and same prompt.
- Hermes must independently run pytest and a JSON CLI smoke for every final workspace.
- Static site must pass JSON/HTML validation and local/public browser checks.

## Sources / Files Consulted
- `tasks/backlog.md`
- `runs/2026-06-22-bb-001-broken-cli-argument-telemetry-rerun/metrics.json`
- `runs/2026-06-22-bb-001-broken-cli-argument-telemetry-rerun/evidence/run_agent.py`
- `docs/site-data.json`
- `docs/index.html`
- Skill reference: `autonomous-coding-agents/references/coding-agent-battle-benchmark-runs.md`
- Skill reference: `visual-design-and-demos/references/evidence-dashboard-github-pages.md`
