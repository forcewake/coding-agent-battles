# Telemetry Extraction — BB-001 Telemetry Rerun

Date: 2026-06-22

This run was created to validate telemetry plumbing after the first BB-001 smoke run. It adds Pi Coding Agent, fixes Claude Code JSON telemetry, and re-tests agy / Antigravity token export.

## Pi Coding Agent

Installed package:

```bash
npm install -g --ignore-scripts @earendil-works/pi-coding-agent@latest
pi --version  # 0.79.10
```

Pi auth was configured locally from an existing Z.AI coding-plan credential. The credential file is not committed.

Run command shape:

```bash
pi --provider zai-coding-cn --model glm-5.2 --thinking xhigh \
  --mode json --no-context-files --approve \
  --tools read,write,edit,bash,grep,find,ls \
  -p <prompt>
```

Telemetry source:

- `agents/pi/agent-output.jsonl` — Pi JSONL stream with per-assistant-message `usage`.
- Tokscale recognizes the session under client `pi`:
  - session id: `019eef5d-c7b6-72e2-85b0-2b1ed456265b`
  - model/provider: `glm-5.2` / `zai-coding-cn`

Observed totals:

```json
{
  "input": 4116,
  "output": 1058,
  "reasoning": 0,
  "cache_read": 20736,
  "cache_write": 0,
  "total": 25910,
  "tokscale_estimated_cost_usd": 0.01580896
}
```

Pi provider JSON reports cost `0` for the Z.AI plan, while Tokscale provides a pricing estimate. Both values are stored in `metrics.json`.

## Claude Code

Previous issue: the first BB-001 run used plain text output and `--no-session-persistence`, so cost/tokens could not be reconstructed after the fact.

Fixed invocation:

```bash
claude --print --output-format json \
  --dangerously-skip-permissions \
  --no-session-persistence \
  --max-budget-usd 1.00 \
  <prompt>
```

Telemetry source:

- `agents/claude-code/agent-output.json`

Observed fields:

```json
{
  "session_id": "7fa30c93-8dac-4836-b2a5-9cf736514b24",
  "duration_ms": 39571,
  "duration_api_ms": 39066,
  "total_cost_usd": 0.110516,
  "usage": {
    "input_tokens": 5925,
    "cache_read_input_tokens": 119232,
    "output_tokens": 851
  },
  "modelUsage": {
    "glm-5.2[1m]": {
      "inputTokens": 5925,
      "outputTokens": 851,
      "cacheReadInputTokens": 119232,
      "cacheCreationInputTokens": 0,
      "costUSD": 0.110516
    }
  }
}
```

Conclusion: Claude telemetry is fixed for future runs as long as the harness always saves JSON output.

## Antigravity agy

Run command shape:

```bash
agy --print \
  --dangerously-skip-permissions \
  --print-timeout 10m \
  --log-file agents/agy/agy-cli.log \
  <prompt>
```

Telemetry attempts:

1. `agy --log-file`: produced useful CLI logs, but no token/cost fields.
2. Local transcript discovery:
   - transcript path: `~/.gemini/antigravity-cli/brain/19b87b1e-f3a8-4ca6-af52-861e73175fd4/.system_generated/logs/transcript_full.jsonl`
   - transcript contains process events (`PLANNER_RESPONSE`, `LIST_DIRECTORY`, `VIEW_FILE`, `RUN_COMMAND`, `CODE_ACTION`) but no reliable token/cost usage.
3. Repeated Tokscale sync while agy was active:

```bash
npx --yes tokscale@latest antigravity sync
```

Every sync reported:

```text
known sessions: 0
detected connections: 0
detected sessions: 0
filesystem candidates: 0
export candidates: 0
cached sessions after sync: 0
```

Conclusion: this installed agy path currently supports **process telemetry** but not reliable token/cost telemetry. The report marks those fields explicitly unavailable rather than estimating from transcript length.

## OpenCode / MiMoCode / Codex

Extraction paths stayed the same as the first BB-001 run:

- OpenCode: direct SQLite extraction from `~/.local/share/opencode/opencode.db`, matched by workspace directory; session `ses_110a248a5ffeyCA5ziakXzEXoa`.
- MiMoCode: direct SQLite extraction from `~/.local/share/mimocode/mimocode.db`, matched by workspace directory; session `ses_110a24e54ffe8ylIFek2PowbW8`.
- Codex CLI: `ccusage codex session --json` and Tokscale cross-check; session `019eef5d-c2f2-7a82-aa3f-c8c28edda010`.

## Redaction

No API keys, OAuth tokens, credential files, or local auth JSON contents were copied into this run directory.
