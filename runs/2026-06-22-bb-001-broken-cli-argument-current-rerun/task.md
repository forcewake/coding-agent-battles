# BB-001 — Broken CLI argument

## Objective

Fix a small Python CLI regression. The `wordfreq` command should accept `--min-length N` and filter out words shorter than `N`, while preserving the existing default behavior.

## Starting point

- Repository fixture: `tasks/BB-001-broken-cli-argument/fixture`
- Setup command: `python -m venv .venv && . .venv/bin/activate && pip install -e . pytest`
- Test command: `pytest -q`
- Smoke command: `python -m bb001_wordfreq --min-length 4 sample.txt`

## Same prompt for all agents

```text
You are in a small Python CLI repository. Fix BB-001.

Goal: make the `wordfreq` CLI accept `--min-length N` as an integer option. It should filter out words shorter than N. Preserve current behavior when the flag is omitted. Do not rewrite the project or change the public output format.

Constraints:
- Keep the change minimal.
- Run the test suite with `pytest -q` before finishing.
- If you add or change tests, keep them focused on the CLI behavior.
- Return a short summary of changed files and verification command output.
```

## Acceptance criteria

- [ ] `pytest -q` passes.
- [ ] `python -m bb001_wordfreq --min-length 4 sample.txt` exits 0.
- [ ] Output format remains `word<TAB>count` sorted by count descending then word ascending.
- [ ] Default behavior without `--min-length` still includes all words.

## Scoring rubric

| Category | Weight | Notes |
|---|---:|---|
| Correctness | 45 | Parses integer option and filters words correctly |
| Verification discipline | 25 | Actually runs `pytest -q` / smoke |
| Minimality | 15 | Small targeted diff |
| Autonomy | 10 | No human help required |
| Time/cost | 5 | Fast and cheap |
