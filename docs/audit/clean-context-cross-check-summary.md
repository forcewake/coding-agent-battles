# Clean-context cross-check — Gemini 3.1 Pro High + MiMO

## Inputs

- Commit reviewed: `49ac381a1f86ede7c0f82168d9012b15f14b5549`
- Review worktree: detached clean worktree, no chat history supplied
- Prompt: `/tmp/cab-clean-review-prompt.md` during execution

## Results

| Reviewer | Verdict | Blockers | Major | Minor |
|---|---|---:|---:|---:|
| Gemini 3.1 Pro High | `APPROVE_WITH_NOTES` | 0 | 0 | 0 |
| MiMO / GLM-5.2 max | `REQUEST_CHANGES` | 0 | 4 | 4 |

## Gemini missing-before-publication-grade

- Rerun legacy scenarios (BB-001 and BB-003) to ensure all agents produce a uniform `result.json` artifact.
- Rerun legacy scenarios to capture row-level telemetry provenance for cost and tokens.
- Implement reliable token and cost export telemetry for the Antigravity (agy) agent.
- Expand the benchmark with additional scenarios before asserting broad, generalized capability rankings.

## MiMO missing-before-publication-grade

- Resolve the duplicate BB-001 dataset: remove or supersede docs/runs/2026-06-22-bb-001-broken-cli-argument/ (and its mirror under runs/) so only the authoritative rerun is public, and remove/scrub references to uncommitted private provider DBs and logs.
- Fix the false agents.html “Pass rate is tied / 100% pass rate” headline (agy is 10/12) and surface real per-agent pass rates on that page.
- Refresh README to the 12-scenario corpus, correct the agy model label, and disclose the shared-model configuration.
- Add an up-front model-pricing caveat to the cost KPI and “Cheapest” badge so cost rankings are not read as pure scaffold comparisons.
- Regenerate or re-stamp the claim ledger and telemetry-provenance manifest at the published commit (populate source_commit).
- Commit sanitized exports (ccusage JSON / provider extracts) for the rows currently marked *_not_raw_committed so the 50 non-raw cost/token rows become third-party-validatable from public files; today only 10/72 rows are committed_raw_agent_json.
- Optional: label “Fastest = fastest passing” on scenario cards and clarify BB-009 where the fastest-finishing attempt failed.

## Controller triage

- Gemini found no issue-level blockers/majors/minors and restated known strategic gaps.
- MiMO found real static/publication issues not covered by the deterministic ledger: false agents-page headline, duplicate public BB-001 dataset, stale README/latestScenario, missing cost/model caveats, ambiguous fastest/cheapest labels, and audit commit stamping nuance.
- This follow-up commit fixes the static/publication issues and removes the duplicate public BB-001 dataset. Remaining strategic gaps are: rerun BB-001/BB-003 with current harness, implement agy telemetry, and publish sanitized raw telemetry exports for local-provider rows.
