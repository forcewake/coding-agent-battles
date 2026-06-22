# Metrics — BB-001 Telemetry Rerun

This rerun adds **Pi Coding Agent**, fixes **Claude Code telemetry**, and re-tests **agy / Antigravity telemetry export**.

## Scoreboard

| Rank by time | Agent | Wall-clock | Tokens total | Cost | Final patch | Process quality | Notes |
|---:|---|---:|---:|---:|---:|---:|---|
| 1 | OpenCode / GLM-5.2 | 35.587s | 63,995 | $0.00 vendor-reported | 100 | 88 | Fastest; pytest + CLI smoke; no red-test capture |
| 2 | Claude Code / GLM-5.2 | 40.680s | 126,008 | $0.110516 reported | 100 | 74 | JSON telemetry fixed; raw tool trace still opaque |
| 3 | MiMoCode / GLM-5.2 | 63.621s | 128,610 | $0.00 vendor-reported | 100 | 78 | Correct; green pytest only in agent log |
| 4 | Pi Coding Agent / GLM-5.2 | 70.733s | 25,910 | ~$0.015809 estimated | 100 | 96 | Best telemetry/process mix: JSONL + red/green + CLI smoke |
| 5 | Codex CLI / GPT-5.5 | 114.752s | 318,536 | ~$0.47–$0.51 estimated | 100 | 87 | Strong red-green; high token overhead |
| 6 | agy / Gemini 3.5 Flash Medium | 191.826s | n/a | n/a | 100 | 80 | Correct; token/cost export still unavailable |

## Token details

| Agent | Input | Output | Reasoning | Cache read | Cache write | Total | Source |
|---|---:|---:|---:|---:|---:|---:|---|
| OpenCode | 3,387 | 917 | 171 | 59,520 | 0 | 63,995 | OpenCode SQLite + Tokscale cross-check |
| Claude Code | 5,925 | 851 | n/a | 119,232 | 0 | 126,008 | `claude --output-format json` / `modelUsage` |
| MiMoCode | 22,501 | 820 | 137 | 105,152 | 0 | 128,610 | MiMoCode SQLite direct extraction |
| Pi Coding Agent | 4,116 | 1,058 | 0 | 20,736 | 0 | 25,910 | Pi `--mode json` + Tokscale cross-check |
| Codex CLI | 41,999 | 4,025 | 1,404 | 272,512 | 0 | 318,536 | `ccusage codex session --json`; Tokscale cross-check |
| agy | n/a | n/a | n/a | n/a | n/a | n/a | No reliable usage fields exposed |

## Cost details

| Agent | Cost field | Value | Interpretation |
|---|---|---:|---|
| OpenCode | vendor-reported | $0.0000 | Z.AI coding-plan logs cost=0; not proof of free compute |
| Claude Code | JSON reported | $0.110516 | Fixed: `--output-format json` exposes `total_cost_usd` |
| MiMoCode | vendor-reported | $0.0000 | Z.AI coding-plan logs cost=0; not proof of free compute |
| Pi Coding Agent | provider JSON | $0.0000 | ZAI provider reports zero plan cost |
| Pi Coding Agent | Tokscale estimate | $0.01580896 | Pricing estimate from Pi local session/JSONL data |
| Codex CLI | ccusage estimate | $0.467001 | Estimated from Codex JSONL |
| Codex CLI | Tokscale estimate | $0.509121 | Independent estimate, different pricing snapshot |
| agy | unavailable | n/a | No reliable local/exported cost source found |

## agy telemetry finding

I tried three routes for agy:

1. `agy --log-file <path>` — useful for CLI logs, but no token/cost fields.
2. Local transcript discovery under `~/.gemini/antigravity-cli/brain/<id>/.system_generated/logs/transcript_full.jsonl` — gives process/tool evidence, no reliable token/cost usage.
3. `tokscale antigravity sync` while the agy run was active — repeated sync attempts still returned:

```text
known sessions: 0
detected connections: 0
detected sessions: 0
filesystem candidates: 0
export candidates: 0
cached sessions after sync: 0
```

Conclusion: for this installed agy/Antigravity CLI path, process telemetry is recoverable, but token/cost telemetry is still **unavailable**. This matches the public Antigravity feature request asking for machine-readable OTLP/token export.

## Claude fix

Previous Claude run used plain text + `--no-session-persistence`, so telemetry was unrecoverable. This rerun uses:

```bash
claude --print --output-format json --dangerously-skip-permissions --no-session-persistence --max-budget-usd 1.00 <prompt>
```

The resulting JSON includes:

- `duration_ms`
- `duration_api_ms`
- `session_id`
- `total_cost_usd`
- `usage`
- `modelUsage`

## Pi addition

Pi was installed as:

```bash
npm install -g --ignore-scripts @earendil-works/pi-coding-agent@latest
```

Run mode:

```bash
pi --provider zai-coding-cn --model glm-5.2 --thinking xhigh --mode json --no-context-files --approve --tools read,write,edit,bash,grep,find,ls -p <prompt>
```

Pi JSONL gives per-message `usage`, and Tokscale recognizes the Pi session under client `pi`.

## Interpretation

All six produced the same final one-line patch, so patch quality is tied. The useful signal in this calibration run is telemetry/process:

- **Pi** has the best combination of low tokens, structured JSONL, red-green, and CLI smoke.
- **OpenCode** remains the fastest.
- **Claude** is now economically comparable because JSON telemetry is fixed.
- **Codex** is process-disciplined but expensive for a trivial task.
- **agy** is usable for process evidence but still weak for economics until token export exists.
