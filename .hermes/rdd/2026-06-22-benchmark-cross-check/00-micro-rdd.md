# Micro-RDD — Benchmark cross-check audit pack

Topology: micro

## Scope
Build and run a deterministic + Gemini High cross-check for Coding Agent Battles public benchmark claims.

## Evidence gathered
- Preflight clean at repo `/home/forcewake/coding-agent-battles-init` on `main`.
- Deterministic audit compares `docs/site-data.json`, `docs/runs/**`, `runs/**`, per-agent result/verify logs, and public rendered scenario pages.
- Gemini 3.1 Pro (High) was run through `agy 1.0.10` against the audit prompt and repo.

## Files changed
- `scripts/audit_claim_ledger.py`
- `scripts/build_telemetry_provenance.py`
- `scripts/extract_bulk_telemetry.py`
- `scripts/recompute_execution_scores.py`
- `docs/audit/*`
- `docs/site-data.json`
- `docs/metrics.md`
- `docs/index.html`
- `docs/app.js`
- `docs/styles.css`
- generated scenario/run docs under `docs/` and `runs/`

## Key decisions
- Keep private provider stores/logs out of the public repo; publish sanitized telemetry provenance levels instead.
- Fix Codex normalized public cost to include reasoning tokens as output tokens while preserving `vendorCost` separately.
- Remove token/cost telemetry from Execution Quality so agents are not penalized for benchmark-tool telemetry gaps.
- Surface BB-001/BB-003 as legacy provenance-gap scenarios instead of fabricating missing `result.json` artifacts.

## Verification commands
```bash
python scripts/extract_bulk_telemetry.py
python scripts/recompute_execution_scores.py
python scripts/build_telemetry_provenance.py
python scripts/audit_claim_ledger.py --public
agy --model "Gemini 3.1 Pro (High)" --dangerously-skip-permissions --add-dir /home/forcewake/coding-agent-battles-init --print-timeout 20m --print "$(cat docs/audit/llm-review-prompt.md)"
```

## Final status before commit
- Deterministic audit: `PASS_WITH_WARNINGS`, 788 PASS / 32 WARN / 0 FAIL.
- Gemini final verdict: `APPROVE_WITH_NOTES`, 0 blockers.
- Accepted notes: BB-001/BB-003 legacy artifact/provenance gaps; OpenCode breakdown-vs-total provider accounting nuance; some telemetry not raw-replayable from public files.
