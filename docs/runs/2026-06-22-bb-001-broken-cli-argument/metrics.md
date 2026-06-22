# Metrics — BB-001 Broken CLI Argument

This augments `results.md` with cost/token/process/quality collection.

## What we now collect

For each run, collect:

- **Outcome:** pass/fail/partial, accepted changes.
- **Correctness:** baseline red, Hermes verification, smoke output.
- **Efficiency:** wall-clock, messages/turns, tool calls.
- **Tokens:** input, output, reasoning, cache read/write, total.
- **Cost:** actual vendor cost where available; otherwise explicit estimate/unavailable.
- **Quality:** final patch quality and process quality as separate scores.
- **Human load:** interventions/retries/manual patches.

Detailed schema: [`../../docs/metrics.md`](../../docs/metrics.md)

## BB-001 scoreboard

| Rank by time | Agent | Wall-clock | Tokens total | Cost | Final patch | Execution quality | Notes |
|---:|---|---:|---:|---:|---:|---:|---|
| 1 | OpenCode / GLM-5.2 | 46.130s | 63,462 | $0.00 vendor-reported | 100 | 86 | Fastest; pytest + CLI smoke; no red-test capture |
| 2 | Claude Code | 68.772s | n/a | n/a | 100 | 72 | Correct patch; original run lacks structured telemetry/raw steps |
| 3 | Codex CLI / GPT-5.5 | 116.323s | 257,358 | ~$0.55–$0.59 estimated | 100 | 84 | Strong red-green; high token overhead from skills/context |
| 4 | MiMoCode / GLM-5.2 | 129.528s | 281,974 | $0.00 vendor-reported | 100 | 91 | Best execution evidence: red + green + CLI smoke |
| 5 | agy / Gemini 3.5 Flash Medium | 332.324s | n/a | n/a | 100 | 78 | Correct and red-green; no reliable token/cost extraction |

## Token details

| Agent | Input | Output | Reasoning | Cache read | Cache write | Total | Source |
|---|---:|---:|---:|---:|---:|---:|---|
| OpenCode | 3,406 | 881 | 295 | 58,880 | 0 | 63,462 | OpenCode SQLite + Tokscale cross-check |
| MiMoCode | 23,426 | 971 | 169 | 257,408 | 0 | 281,974 | MiMoCode SQLite direct extraction |
| Codex CLI | 69,047 | 3,735 | 1,491 | 184,576 | 0 | 257,358 | `ccusage codex session --json`; Codex JSONL token events |
| Claude Code | n/a | n/a | n/a | n/a | n/a | n/a | Original run used plain text + `--no-session-persistence` |
| agy | n/a | n/a | n/a | n/a | n/a | n/a | agy transcript did not expose reliable usage fields |

## Cost details

| Agent | Cost field | Value | Interpretation |
|---|---|---:|---|
| OpenCode | vendor-reported | $0.0000 | Z.AI coding-plan logs token counts but cost=0; do **not** interpret as free compute |
| MiMoCode | vendor-reported | $0.0000 | Same Z.AI coding-plan caveat |
| Codex CLI | ccusage estimate | $0.549573 | Estimated from local Codex JSONL + public pricing |
| Codex CLI | Tokscale estimate | $0.594303 | Independent estimate, slightly different pricing snapshot |
| Claude Code | unavailable | n/a | Use `--output-format json` in future |
| agy | unavailable | n/a | Tokscale Antigravity sync found no exported/live sessions for this run |

## Quality interpretation

All five produced the same correct one-line patch, so **final patch quality is tied at 100/100**. The differentiator is process quality:

- **MiMoCode** had the strongest evidence trail: reproduced failure, fixed, reran tests, and smoke-tested default + `--min-length` behavior.
- **OpenCode** was fastest and smoke-tested, but edited before capturing a red run.
- **Codex CLI** followed red-green carefully, but burned substantially more tokens by loading multiple process skills and did not do an agent-owned CLI smoke.
- **agy** reproduced red and green but was slow and did not expose token/cost telemetry.
- **Claude Code** solved correctly, but the original harness invocation hid raw execution, tokens, and cost.

## Harness fixes for future runs

- Run **Claude Code** with `--output-format json` and save the JSON result.
- Run **Codex CLI** with `--json` or preserve its session id, then extract with `ccusage codex session --json` / Tokscale.
- For **OpenCode/MiMoCode**, query SQLite by workspace/session immediately after run and save sanitized token totals.
- For **agy**, keep transcript paths and try Tokscale sync, but mark tokens/cost unavailable unless explicit fields are found.
- Store both `metrics.json` and `metrics.md` in every run folder.
