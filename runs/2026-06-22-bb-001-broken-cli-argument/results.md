# Results — BB-001 Broken CLI Argument

Date: 2026-06-22

## Task

Fix the `wordfreq` Python CLI so `--min-length N` is parsed as an integer option and filters out words shorter than `N`, while preserving default output.

Baseline was intentionally red:

```text
FAILED tests/test_cli.py::test_min_length_filters_short_words
wordfreq: error: unrecognized arguments: .../sample.txt
[baseline_exit_code] 1
```

## Prompt

All agents received the same prompt from `evidence/prompt.txt`.

## Agent versions

| Agent | Version observed |
|---|---|
| MiMoCode | `mimo 0.1.1` |
| OpenCode | `opencode 1.17.6` |
| Antigravity agy | `agy 1.0.10` |
| Claude Code | `2.1.177` |
| Codex CLI | `codex-cli 0.137.0` |

## Summary

| Agent | Agent exit | Agent wall-clock | Hermes verification | Changed files | Verdict |
|---|---:|---:|---|---:|---|
| OpenCode | 0 | 46.130s | `pytest -q` + CLI smoke passed | 1 | PASS |
| Claude Code | 0 | 68.772s | `pytest -q` + CLI smoke passed | 1 | PASS |
| Codex CLI | 0 | 116.323s | `pytest -q` + CLI smoke passed | 1 | PASS |
| MiMoCode | 0 | 129.528s | `pytest -q` + CLI smoke passed | 1 | PASS |
| agy | 0 | 332.324s | `pytest -q` + CLI smoke passed | 1 | PASS |

Cost/token/process/quality data has now been collected in:

- [`metrics.md`](metrics.md) — human-readable scoreboard
- [`metrics.json`](metrics.json) — machine-readable metrics

Short version: OpenCode and MiMo expose GLM token counts via local SQLite; Codex exposes token/cost estimates via local JSONL + `ccusage`/Tokscale; Claude Code's original plain-text `--no-session-persistence` run is not recoverable for tokens/cost; agy's local transcript did not expose reliable cost/tokens.

## Independent verification command

Hermes reran this in every agent workspace, after deleting `.venv`:

```bash
rm -rf .venv && python -m venv .venv && . .venv/bin/activate && pip install -q -e . pytest && pytest -q && python -m bb001_wordfreq --min-length 4 sample.txt
```

All five produced:

```text
..                                                                       [100%]
2 passed in 0.06s
beta	2
elephant	2
alpha	1
[verify_exit_code] 0
```

## Diff pattern

All five agents made the same minimal fix in `bb001_wordfreq/cli.py`:

```diff
-        action="store_true",
+        type=int,
```

## Artifacts

Per-agent folders under `agents/<agent>/` contain:

- `workspace/` — isolated final workspace
- `agent.log` — raw agent output
- `agent-meta.txt` — command, exit code, wall-clock
- `diff.patch` — final diff from broken baseline
- `git-status.txt` — final workspace status
- `verify.log` — independent Hermes verification output

## Notes for next battle

This task is useful as a plumbing smoke: all agents solved it. It is too easy to differentiate code quality, but good for validating isolation, prompt parity, log collection, and independent verification.
