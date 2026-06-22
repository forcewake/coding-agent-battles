# BB-012 — Unknown repo leverage task metrics

## Scope

- Type: External helper leverage
- Difficulty: L4
- Pass count: 6/6
- Execution score: deterministic composite from correctness, red-baseline capture, smoke evidence, independent verification, exit code, telemetry coverage, scenario-local speed percentile, and scenario-local token-efficiency percentile.

## Agent metrics

| Agent | Verdict | Wall | Tokens | Normalized public cost | Patch | Execution score | Notes |
|---|---:|---:|---:|---:|---:|---:|---|
| OpenCode | PASS | 52.259s | 55,799 | $0.023785 | 100 | 96 | execution-quality composite |
| Claude | PASS | 43.710s | 126,638 | $0.042389 | 100 | 92 | execution-quality composite |
| MiMo | PASS | 64.967s | 213,715 | $0.065665 | 100 | 80 | execution-quality composite |
| Pi | PASS | 86.329s | 38,848 | $0.015392 | 100 | 89 | execution-quality composite |
| Codex | PASS | 90.124s | 167,667 | $0.424154 | 100 | 77 | execution-quality composite |
| agy | PASS | 102.463s | n/a | n/a | 100 | 69 | execution-quality composite |
