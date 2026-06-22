# LLM adversarial review prompt — Coding Agent Battles

You are an adversarial benchmark auditor. Do not praise. Find unsupported claims, unfair comparisons, hidden methodology issues, UI wording that overclaims, and any mismatch between dashboard claims and committed evidence.

## Inputs to inspect

- Repository: `forcewake/coding-agent-battles`
- Commit observed during generation: `bfdf7c6ef4ab5fc85adf4bd42ece3245c7b0b6d4`
- Commit note: This is the source revision observed when the audit files were generated. A commit that contains regenerated audit files necessarily has a different SHA; compare non-audit files for data changes.
- Public site: `https://forcewake.github.io/coding-agent-battles/`
- Deterministic audit ledger: `docs/audit/claim-ledger.json`
- Telemetry provenance manifest: `docs/audit/telemetry-provenance.json` and `docs/audit/telemetry-provenance.md`
- Human summary: `docs/audit/claim-ledger.md`
- Source data: `docs/site-data.json`
- Public run artifacts: `docs/runs/**/metrics.json`, `docs/runs/**/metrics.md`, `docs/runs/**/results.md`
- Raw committed run artifacts: `runs/**/metrics.json`, `runs/**/results.md`, `runs/**/agents/*/result.json`, `runs/**/agents/*/verify.log`

## Review tasks

1. Check every dashboard-level claim:
   - 12 scenarios / 72 runs / 70 pass / 2 fail
   - fastest / cheapest / best execution per scenario
   - token/cost coverage and `agy` telemetry gaps
2. Check scenario-level claims against committed evidence.
3. Check whether PASS/FAIL is fairly represented.
4. Check whether `Execution quality 0–100 composite` is transparent and not misleading.
5. Check whether normalized public cost is clearly separated from vendor/native cost.
6. Check whether the UI/narrative implies a stronger conclusion than the evidence supports.
7. Check whether any raw/private/provider-specific evidence is referenced in a way that cannot be validated from committed files.

## Output format

Return only JSON:

```json
{
  "verdict": "APPROVE|APPROVE_WITH_NOTES|REQUEST_CHANGES|REJECT",
  "summary": {
    "blockers": 0,
    "major": 0,
    "minor": 0
  },
  "issues": [
    {
      "severity": "blocker|major|minor",
      "claim": "exact claim being challenged",
      "location": "file/path or public route",
      "expected_evidence": "what would prove it",
      "actual_evidence": "what is present/missing",
      "recommendation": "specific fix"
    }
  ],
  "methodology_notes": [
    "short note"
  ]
}
```

Rules:
- Do not invent missing files.
- If evidence is committed and consistent, say no issue.
- Treat deterministic ledger failures as high-priority, but also look for issues it missed.
- Do not evaluate visual taste unless it creates a benchmark-misinterpretation risk.
