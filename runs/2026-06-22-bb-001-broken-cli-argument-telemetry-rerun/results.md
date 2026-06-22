# Results — BB-001 Telemetry Rerun

Date: 2026-06-22

## Task

Fix the `wordfreq` Python CLI so `--min-length N` is parsed as an integer option and filters out words shorter than `N`, while preserving default output.

Baseline was intentionally red:

```text
FAILED tests/test_cli.py::test_min_length_filters_short_words
wordfreq: error: unrecognized arguments: .../sample.txt
[baseline_exit_code] 1
```

## What changed in this rerun

- Added **Pi Coding Agent** as a sixth participant.
- Fixed **Claude Code telemetry** by running it with `--output-format json` and saving `agent-output.json`.
- Tested **agy / Antigravity telemetry** via `--log-file`, local transcript discovery, and repeated `tokscale antigravity sync` while the run was active.
- Saved per-run cost/token/process/quality data in [`metrics.md`](metrics.md) and [`metrics.json`](metrics.json).

## Agent versions

| Agent | Version observed |
|---|---|
| OpenCode | `opencode 1.17.6` |
| Claude Code | `2.1.177` |
| MiMoCode | `mimo 0.1.1` |
| Pi Coding Agent | `pi 0.79.10` |
| Codex CLI | `codex-cli 0.137.0` |
| Antigravity agy | `agy 1.0.10` |

## Summary

| Agent | Agent exit | Agent wall-clock | Hermes verification | Changed files | Verdict |
|---|---:|---:|---|---:|---|
| OpenCode | 0 | 35.587s | `pytest -q` + CLI smoke passed | 1 | PASS |
| Claude Code | 0 | 40.680s | `pytest -q` + CLI smoke passed | 1 | PASS |
| MiMoCode | 0 | 63.621s | `pytest -q` + CLI smoke passed | 1 | PASS |
| Pi Coding Agent | 0 | 70.733s | `pytest -q` + CLI smoke passed | 1 | PASS |
| Codex CLI | 0 | 114.752s | `pytest -q` + CLI smoke passed | 1 | PASS |
| agy | 0 | 191.826s | `pytest -q` + CLI smoke passed | 1 | PASS |

## Independent verification command

Hermes reran this in every agent workspace, after deleting transient state:

```bash
rm -rf .venv .pytest_cache bb001_wordfreq.egg-info __pycache__ */__pycache__
python -m venv .venv
. .venv/bin/activate
pip install -q -e . pytest
pytest -q
python -m bb001_wordfreq --min-length 4 sample.txt
```

All six produced:

```text
..                                                                       [100%]
2 passed
beta	2
elephant	2
alpha	1
[verify_exit_code] 0
```

## Diff pattern

All six agents made the same minimal fix in `bb001_wordfreq/cli.py`:

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
- JSON telemetry where available (`agent-output.json` / `agent-output.jsonl`)

## Notes

This remains a calibration/plumbing task. It now validates the telemetry harness better than the coding quality dimension, because all agents produce the same one-line patch.
