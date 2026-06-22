# Coding Agent Battle Metrics

This repo treats a coding-agent run as an end-to-end engineering attempt, not just a patch diff.

## Required metrics per agent run

| Layer | Metric | Why it matters | Source |
|---|---|---|---|
| Identity | agent, CLI version, model/provider, invocation | Reproducibility; separates scaffold from model | `agent-meta.txt`, CLI `--version`, DB/session logs |
| Outcome | pass/fail/partial, accepted change count | Comparable pass@1 style result | Hermes verification logs |
| Correctness | baseline red, tests pass, smoke pass, hidden/extra checks if available | Avoids trusting agent self-report | `baseline-failure.log`, `verify.log`, browser/CLI/API smoke |
| Quality | final patch quality, process quality, evidence transparency | Distinguishes identical green patches from sloppy execution | `diff.patch`, agent log, reviewer rubric |
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

### Process quality score, 0–100

| Dimension | Weight |
|---|---:|
| Agent-owned verification discipline | 35 |
| Root-cause clarity | 20 |
| Evidence transparency / raw logs | 20 |
| Efficiency relative to task complexity | 15 |
| Autonomy / no human intervention | 10 |

## Cost and token collection notes

- **OpenCode** stores per-session tokens in `~/.local/share/opencode/opencode.db`; `opencode stats` is useful, but at the time of this run it has no JSON output, so direct SQLite extraction or tools such as Tokscale are better for automation.
- **MiMoCode** stores compatible session data in `~/.local/share/mimocode/mimocode.db`; use direct SQLite extraction until a stable JSON stats endpoint exists.
- **Codex CLI** stores JSONL under `~/.codex/sessions/`; `ccusage codex session --json` and Tokscale can estimate tokens/cost from those logs.
- **Claude Code** can emit structured per-run JSON with `claude --print --output-format json`; if a run was executed as plain text with `--no-session-persistence`, per-run cost/tokens are not recoverable afterwards.
- **Pi Coding Agent** can emit JSONL with `pi --mode json`; Tokscale recognizes Pi sessions under client `pi`, so use both Pi JSONL and Tokscale as cross-checks.
- **Antigravity agy** currently exposes rich local transcripts under `~/.gemini/antigravity-cli/brain/...`, but this run did not expose reliable token/cost fields. `tokscale antigravity sync` returned zero sessions even when run repeatedly during an active CLI run; mark unavailable instead of estimating from transcript size.

## Source inspiration

- Artificial Analysis Coding Agent Index methodology: pass@1, cost, token usage, execution time and reliability across realistic coding-agent components.
- SWE-bench: resolved percentage and trajectory artifacts for real issue resolution.
- LongCLI-Bench: F2P/P2P tests plus step-level scoring for partial progress.
- GitTaskBench: end-to-end task success, output quality, cost, and economic-value style metrics.
- ccusage / Tokscale docs: local session-log extraction for Codex/OpenCode/Claude-style coding tools.
