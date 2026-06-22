# BB-009 — Observability instrumentation metrics

## Scope

- Type: Non-functional backend
- Difficulty: L3
- Pass count: 5/6
- Execution score: deterministic composite from correctness, red-baseline capture, smoke evidence, independent verification, exit code, telemetry coverage, scenario-local speed percentile, and scenario-local token-efficiency percentile.

## Agent metrics

| Agent | Verdict | Wall | Tokens | Normalized public cost | Patch | Execution score | Notes |
|---|---:|---:|---:|---:|---:|---:|---|
| OpenCode | PASS | 58.357s | 87,637 | $0.030313 | 100 | 92 | execution-quality composite |
| Claude | PASS | 89.627s | 153,562 | $0.052263 | 100 | 80 | execution-quality composite |
| MiMo | PASS | 91.989s | 283,029 | $0.097538 | 100 | 72 | execution-quality composite |
| Pi | PASS | 68.880s | 19,534 | $0.013878 | 100 | 93 | execution-quality composite |
| Codex | PASS | 100.717s | 197,851 | $0.438998 | 100 | 75 | execution-quality composite |
| agy | FAIL | 43.784s | n/a | n/a | 0 | 34 | execution-quality composite |
