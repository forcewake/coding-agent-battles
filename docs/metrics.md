# Coding Agent Battle Metrics

This repo treats a coding-agent run as an end-to-end engineering attempt, not just a patch diff.

## Required metrics per agent run

| Layer | Metric | Why it matters | Source |
|---|---|---|---|
| Identity | agent, CLI version, model/provider, invocation | Reproducibility; separates scaffold from model | `agent-meta.txt`, CLI `--version`, DB/session logs |
| Outcome | pass/fail/partial, accepted change count | Comparable pass@1 style result | Hermes verification logs |
| Correctness | baseline red, tests pass, smoke pass, hidden/extra checks if available | Avoids trusting agent self-report | `baseline-failure.log`, `verify.log`, browser/CLI/API smoke |
| Quality | final patch quality, execution-quality composite, evidence transparency | Distinguishes identical green patches from sloppy or expensive execution | `diff.patch`, verification logs, telemetry, wall-clock |
| Efficiency | wall-clock, turns/messages, tool calls, retries | Agent/scaffold productivity and latency | `agent-meta.txt`, session DB/JSONL/transcript |
| Tokens | input, output, reasoning, cache read/write, total | Primary resource consumption | local session logs/DBs, `ccusage`, `tokscale`, vendor JSON |
| Cost | actual billed cost if available; otherwise explicit estimate/unavailable | Cost-per-accepted-change and budget control | vendor JSON, LiteLLM/ccusage/tokscale estimates |
| Human load | interventions, approvals, manual restarts, prompt changes | Autonomy signal | controller notes |
| Safety/hygiene | files changed, secrets scan, generated trash, off-limits edits | Prevents benchmark wins via unsafe side effects | git diff/status, scans |

## Quality rubric

Use two scores so we do not hide a perfect one-line patch behind bad/opaque process:

### Final patch score, 0–100

| Dimension | Weight |
|---|---:|
| Functional correctness against acceptance criteria | 45 |
| Regression preservation | 20 |
| Minimality / maintainability | 20 |
| Safety / no unrelated side effects | 15 |

### Execution-quality composite, 0–100

| Dimension | Weight |
|---|---:|
| Correct final result (`PASS`) | 40 |
| Captured failing baseline (`red✓`) | 15 |
| Ran scenario smoke / user-visible proof (`smoke✓`) | 15 |
| Independent verifier passed | 15 |
| Agent process exited cleanly | 5 |
| Scenario-local speed percentile | 10 |

Execution quality deliberately excludes token/cost telemetry. Efficiency is shown separately in token and cost panels so agents are not penalized for benchmark tooling gaps such as unavailable Antigravity telemetry.

## Cost and token collection notes

`ccusage` is the preferred first-pass collector for every supported local coding-agent data source. Use source-focused JSON reports such as:

```bash
npx --yes ccusage@latest claude session --json
npx --yes ccusage@latest codex session --json
npx --yes ccusage@latest opencode session --json
npx --yes ccusage@latest hermes session --json
npx --yes ccusage@latest pi session --json
npx --yes ccusage@latest gemini session --json
```

Run attribution still matters: if a ccusage report aggregates a source/day but does not expose enough workspace/session metadata to tie a row to a specific benchmark run, save the ccusage output as cross-check evidence and fall back to the raw source that can be matched by workspace/session id.

- **OpenCode**: primary `ccusage opencode session --json`; fallback/cross-check direct local OpenCode store matched by workspace directory.
- **MiMoCode**: not currently a ccusage focused namespace; use direct local MiMoCode SQLite extraction until a compatible ccusage/source adapter exists.
- **Codex CLI**: primary `ccusage codex session --json`; fallback/cross-check local Codex JSONL token events when available.
- **Claude Code**: primary `ccusage claude session --json` when persistent Claude project logs exist; fallback per-run `claude --print --output-format json` when the harness intentionally disables session persistence.
- **Pi Coding Agent**: primary `ccusage pi session --json`; fallback/cross-check Pi `--mode json` JSONL and Tokscale.
- **Hermes Agent**: `ccusage hermes session --json` can report Hermes controller-session usage from `$HERMES_HOME/state.db`; keep this separate from participant-agent economics unless explicitly measuring controller overhead.
- **Gemini CLI**: `ccusage gemini session --json` supports Gemini CLI logs under `~/.gemini/tmp/*/chats/`. This is not the same as Antigravity `agy` transcripts under `~/.gemini/antigravity-cli/brain/...`.
- **Antigravity agy**: current runs expose process transcripts, but no reliable token/cost fields via ccusage/Tokscale for this installed path; mark unavailable instead of estimating from transcript size.

## Source inspiration

- Artificial Analysis Coding Agent Index methodology: pass@1, cost, token usage, execution time and reliability across realistic coding-agent components.
- SWE-bench: resolved percentage and trajectory artifacts for real issue resolution.
- LongCLI-Bench: F2P/P2P tests plus step-level scoring for partial progress.
- GitTaskBench: end-to-end task success, output quality, cost, and economic-value style metrics.
- ccusage / Tokscale docs: local session-log extraction for Codex/OpenCode/Claude-style coding tools.
