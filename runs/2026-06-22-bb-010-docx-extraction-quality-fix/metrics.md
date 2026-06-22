# BB-010 — DOCX extraction quality fix metrics

## Scope

- Type: Document extraction
- Difficulty: L3
- Pass count: 6/6
- Execution score: deterministic composite from correctness, red-baseline capture, smoke evidence, independent verification, exit code, telemetry coverage, scenario-local speed percentile, and scenario-local token-efficiency percentile.

## Agent metrics

| Agent | Verdict | Wall | Tokens | Normalized public cost | Patch | Execution score | Notes |
|---|---:|---:|---:|---:|---:|---:|---|
| OpenCode | PASS | 67.775s | 81,296 | $0.033141 | 100 | 97 | execution-quality composite |
| Claude | PASS | 69.886s | 157,352 | $0.076082 | 100 | 92 | execution-quality composite |
| MiMo | PASS | 336.866s | 218,039 | $0.073111 | 100 | 74 | execution-quality composite |
| Pi | PASS | 79.757s | 22,809 | $0.019299 | 100 | 99 | execution-quality composite |
| Codex | PASS | 129.014s | 284,455 | $0.496041 | 100 | 82 | execution-quality composite |
| agy | PASS | 103.864s | n/a | n/a | 100 | 82 | execution-quality composite |
