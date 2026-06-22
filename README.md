# Coding Agent Battles

Public logbook for honest head-to-head comparisons of coding-agent **scaffold + model** configurations.

## Current corpus

- Live dashboard: <https://forcewake.github.io/coding-agent-battles/>
- Corpus: **12 scenarios** (`BB-001` through `BB-012`)
- Matrix: **6 agents × 12 scenarios = 72 runs**
- Current aggregate: **70 PASS / 2 FAIL**
- Latest scenario page: <https://forcewake.github.io/coding-agent-battles/scenarios/bb-012.html>
- Audit pack: <https://forcewake.github.io/coding-agent-battles/audit/cross-check-summary.md>

## Participants

| Agent | Model / runtime label | Notes |
|---|---|---|
| OpenCode | GLM-5.2 | Z.AI coding model via OpenCode scaffold |
| Claude Code | GLM-5.2 `[1m]` | Claude Code scaffold configured against GLM-5.2 |
| MiMoCode | GLM-5.2 | Xiaomi MiMoCode scaffold configured against GLM-5.2 |
| Pi Coding Agent | GLM-5.2 | Pi scaffold configured against GLM-5.2 |
| Codex CLI | GPT-5.5 | OpenAI Codex CLI scaffold/model pair |
| Antigravity `agy` | Gemini 3.5 Flash Medium | Antigravity scaffold/model pair; token/cost telemetry unavailable in this corpus |

Interpretation caveat: these are **scaffold + model** comparisons. Four agents share GLM-5.2, while Codex and agy use different model families. Cost and pass/fail should not be read as scaffold-only conclusions until a model-controlled sweep exists.

## What gets compared

Each battle keeps the task, constraints and verification identical across agents.

| Dimension | Evidence to store |
|---|---|
| Task | Prompt, starting repo/commit, allowed tools, timebox |
| Output | Final diff, branch/commit, generated artifacts |
| Correctness | Tests, lint, typecheck, CLI/browser smoke, screenshots where useful |
| Quality | Final patch score, execution-quality score, evidence transparency notes |
| Efficiency | Wall-clock, messages/turns, tool calls, retries |
| Economics | Input/output/reasoning/cache tokens, normalized public estimate, native/vendor cost where available |
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

Per-run reports may still use direct JSON/JSONL/SQLite extraction when ccusage cannot map a focused row back to the benchmark workspace/session. Those direct extracts are fallback/cross-check evidence, not a replacement for ccusage where ccusage has reliable run attribution. Public telemetry limitations are documented in `docs/audit/telemetry-provenance.md`.

## Repository layout

```text
tasks/                 Candidate battle tasks and task specs
runs/                  One folder per executed battle
docs/                  GitHub Pages dashboard and public run artifacts
docs/audit/            Deterministic ledger, telemetry provenance, LLM review outputs
scripts/               Dashboard, telemetry, and audit generation scripts
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
