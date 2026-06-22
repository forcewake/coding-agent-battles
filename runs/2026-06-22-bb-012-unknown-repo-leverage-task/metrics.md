# BB-012 — Unknown repo leverage task metrics

## Scope

- Type: External helper leverage
- Difficulty: L4
- Pass count: 6/6
- Execution score: deterministic composite from correctness, red-baseline capture, smoke evidence, independent verification, clean agent exit, and scenario-local speed percentile. Token/cost telemetry is reported separately and is not part of execution quality.

## Agent metrics

| Agent | Verdict | Wall | Tokens | Normalized public cost | Patch | Execution score | Notes |
|---|---:|---:|---:|---:|---:|---:|---|
| OpenCode | PASS | 52.259s | 55,799 | $0.023785 | 100 | 99 | execution-quality composite |
| Claude | PASS | 43.710s | 126,638 | $0.042389 | 100 | 100 | execution-quality composite |
| MiMo | PASS | 64.967s | 213,715 | $0.065665 | 100 | 96 | execution-quality composite |
| Pi | PASS | 86.329s | 38,848 | $0.015392 | 100 | 93 | execution-quality composite |
| Codex | PASS | 90.124s | 167,667 | $0.451874 | 100 | 92 | execution-quality composite |
| agy | PASS | 102.463s | n/a | n/a | 100 | 90 | execution-quality composite |
