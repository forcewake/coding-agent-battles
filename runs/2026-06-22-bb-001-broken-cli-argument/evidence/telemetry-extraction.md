# Telemetry extraction notes — BB-001

## Commands / sources used

### OpenCode

- Session found by matching workspace directory in `~/.local/share/opencode/opencode.db`.
- Session id: `ses_110d898e8ffemqqPYmGmijGsye`.
- Token totals extracted from assistant message `tokens` fields.
- Cross-check: `tokscale --json --today --group-by client,session,model` returned the same session and token totals.

### MiMoCode

- Session found by matching workspace directory in `~/.local/share/mimocode/mimocode.db`.
- Session id: `ses_110d89e0cffeK6vUi5QDnaQBDd`.
- Token totals extracted from assistant message `tokens` fields.
- `mimo stats --days 1` was not usable for this specific run because the day had many unrelated MiMo sessions.

### Codex CLI

- Session id came from `agents/codex-cli/agent.log`:
  `019eef27-7586-7ef0-b134-26ea116c9312`.
- JSONL file:
  `~/.codex/sessions/2026/06/22/rollout-2026-06-22T13-46-41-019eef27-7586-7ef0-b134-26ea116c9312.jsonl`.
- Token totals cross-checked with:
  - Codex `event_msg` / `token_count` final cumulative event.
  - `ccusage codex session --json`.
  - `tokscale --json --today --group-by client,session,model`.
- Cost is an estimate, not observed billing.

### Claude Code

- Original invocation used plain text output and `--no-session-persistence`.
- Result: no recoverable per-run session JSON/tokens/cost.
- A separate smoke confirmed future runs should use:

```bash
claude --print --output-format json ...
```

That JSON contains `usage`, `modelUsage`, `duration_ms`, `duration_api_ms`, `total_cost_usd`, and `session_id`.

### agy / Antigravity

- Session/transcript found under:
  `~/.gemini/antigravity-cli/brain/94113f4a-f219-45d4-9231-06876274f41a/.system_generated/logs/transcript_full.jsonl`.
- Transcript exposed process/tool evidence, but not reliable token/cost fields.
- `tokscale antigravity sync` found no live/exported sessions:
  - known sessions: 0
  - detected connections: 0
  - detected sessions: 0

## Safety note

Only sanitized aggregate numbers were committed. Raw home-directory DBs/auth files were not copied into the public repo.
