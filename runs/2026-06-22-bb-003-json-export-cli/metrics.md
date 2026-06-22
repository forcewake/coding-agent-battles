# BB-003 — JSON export for existing CLI metrics

## Scope

- Type: CLI feature
- Difficulty: L1
- Pass count: 6/6
- Execution score: deterministic composite from correctness, red-baseline capture, smoke evidence, independent verification, exit code, telemetry coverage, scenario-local speed percentile, and scenario-local token-efficiency percentile.

## Agent metrics

| Agent | Verdict | Wall | Tokens | Normalized public cost | Patch | Execution score | Notes |
|---|---:|---:|---:|---:|---:|---:|---|
| OpenCode | PASS | 66.732s | 149,488 | $0.051295 | 100 | 66 | execution-quality composite |
| Claude | PASS | 52.901s | 156,994 | $0.072912 | 100 | 68 | execution-quality composite |
| MiMo | PASS | 94.151s | 330,730 | $0.108728 | 100 | 53 | execution-quality composite |
| Pi | PASS | 56.314s | 5,512 | $0.002751 | 100 | 74 | execution-quality composite |
| Codex | PASS | 104.966s | 242,829 | $1.430545 | 100 | 66 | execution-quality composite |
| agy | PASS | 147.780s | n/a | n/a | 100 | 44 | execution-quality composite |
