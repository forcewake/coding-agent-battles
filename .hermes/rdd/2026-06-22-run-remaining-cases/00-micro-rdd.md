# Micro-RDD — Run remaining benchmark cases

Topology: swarm

## Request
Run all remaining Coding Agent Battles benchmark cases after BB-001/BB-003.

## Scope
- Added fixtures for BB-002 and BB-004 through BB-012.
- Prepared 10 scenario run directories.
- Ran 6 agents per new scenario: OpenCode, Claude Code, MiMoCode, Pi, Codex CLI, and Antigravity agy.
- Total new runs: 60.

## Execution notes
- Hermes `delegate_task` was not used for implementation because the current Codex/ChatGPT transport rejects the configured `claude-opus-4.7` subagent model.
- Used local CLI agents directly through `scripts/run_remaining_suite.py`.
- Each agent ran in an isolated copied fixture workspace.
- Every run produced `agent.log`, `agent-meta.txt`, `diff.patch`, `git-status.txt`, `verify.log`, and `result.json`.
- Independent verification was always `python verify.py` run by the controller after the agent exited.

## Result
- New suite summary: `runs/2026-06-22-all-remaining-suite-summary.json`
- New runs: 60
- New passes: 58
- New fails: 2
- Harness errors: 0
- Fails:
  - BB-005 / agy: exited 0 but did not enforce `/admin` auth; independent verify failed.
  - BB-009 / agy: exited 0 but did not create required structured request events; independent verify failed.

## Dashboard update
- Aggregate dashboard now covers 12 scenarios / 72 total agent runs / 70 passes.
- Added per-scenario pages for BB-002 and BB-004 through BB-012.
- Token/cost values for the new bulk suite are intentionally `n/a` until a separate telemetry attribution pass is performed; wall-clock/pass-fail values are verified.

## Verification
- All generated fixtures had honest red baselines before agent launch.
- Suite process completed with exit code 0.
- JSON, HTML, and JS syntax checks passed.
- Local HTTP route smoke passed for home, agents, all scenario pages, D3 vendor file, and `site-data.json`.
- Browser console was clean on home, agents, and BB-005 detail page.
- Visual QA passed for home, agents, and BB-005 detail page.
- Secret scan passed with explicit allowlist for synthetic benchmark strings `Bearer wrong` and `Bearer secret-token`.
