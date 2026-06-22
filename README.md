# Coding Agent Battles

Public logbook for honest head-to-head comparisons of coding agents.

## Initial participants

- MiMoCode / GLM-5.2
- OpenCode / GLM-5.2
- Antigravity `agy` / Google AI Pro
- Claude Code
- Codex CLI
- Pi Coding Agent

## What gets compared

Each battle should keep the task, constraints and verification identical across agents.

| Dimension | Evidence to store |
|---|---|
| Task | Prompt, starting repo/commit, allowed tools, timebox |
| Output | Final diff, branch/commit, generated artifacts |
| Correctness | Tests, lint, typecheck, CLI/browser smoke, screenshots where useful |
| Quality | Final patch score, process quality score, evidence transparency notes |
| Efficiency | Wall-clock, messages/turns, tool calls, retries |
| Economics | Input/output/reasoning/cache tokens, actual/estimated cost, cost-per-accepted-change |
| Review | Hermes independent verification notes and final verdict |

## Telemetry collection

`ccusage` is the first-pass collector for supported local coding-agent sources:

```bash
npx --yes ccusage@latest claude session --json
npx --yes ccusage@latest codex session --json
npx --yes ccusage@latest opencode session --json
npx --yes ccusage@latest hermes session --json
npx --yes ccusage@latest pi session --json
npx --yes ccusage@latest gemini session --json
```

Per-run reports may still use direct JSON/JSONL/SQLite extraction when ccusage cannot map a focused row back to the benchmark workspace/session. Those direct extracts are fallback/cross-check evidence, not a replacement for ccusage where ccusage has reliable run attribution.

## Live Pages

- GitHub Pages dashboard: <https://forcewake.github.io/coding-agent-battles/>
- Current view: aggregate home dashboard across BB-001 + BB-003, with Agent × Scenario matrix, agent profiles, Pareto lens, and latest-run detail.
- Latest scenario: BB-003 JSON export for existing CLI — <runs/2026-06-22-bb-003-json-export-cli/results.md>
- Previous calibration: BB-001 telemetry rerun — <runs/2026-06-22-bb-001-broken-cli-argument-telemetry-rerun/results.md>

## Repository layout

```text
tasks/                 Candidate battle tasks and task specs
templates/             Reusable task/run report templates
runs/                  One folder per executed battle
```

Suggested run folder format:

```text
runs/YYYY-MM-DD-task-slug/
  task.md
  results.md
  metrics.md
  metrics.json
  agents/
    mimo/
    opencode/
    agy/
    claude-code/
    codex-cli/
    pi/
  evidence/
```

## Sources / benchmark inspiration

- SWE-bench: real GitHub issue resolution, with Verified/Lite/Full/Multilingual/Multimodal splits — <https://www.swebench.com>
- LongCLI-Bench: long-horizon CLI programming tasks across scratch, feature, bugfix, refactor — <https://github.com/finyorko/longcli-bench>
- GitTaskBench: repo-aware end-to-end tasks using existing GitHub projects — <https://github.com/QuantaAlpha/GitTaskBench>
- AI Agent Benchmark Compendium: broader map of coding/tool/web/GUI agent benchmarks — <https://github.com/philschmid/ai-agent-benchmark-compendium>

Created: 2026-06-22
