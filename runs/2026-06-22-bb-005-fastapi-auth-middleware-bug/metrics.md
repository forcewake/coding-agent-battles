# BB-005 — FastAPI auth middleware bug metrics

## Scope

- Type: Backend debugging
- Difficulty: L2
- Pass count: 5/6
- Execution score: deterministic composite from correctness, red-baseline capture, smoke evidence, independent verification, exit code, telemetry coverage, scenario-local speed percentile, and scenario-local token-efficiency percentile.

## Agent metrics

| Agent | Verdict | Wall | Tokens | Normalized public cost | Patch | Execution score | Notes |
|---|---:|---:|---:|---:|---:|---:|---|
| OpenCode | PASS | 43.633s | 53,635 | $0.023405 | 100 | 100 | execution-quality composite |
| Claude | PASS | 47.969s | 153,526 | $0.050461 | 100 | 99 | execution-quality composite |
| MiMo | PASS | 46.894s | 128,828 | $0.041709 | 100 | 99 | execution-quality composite |
| Pi | PASS | 87.805s | 34,046 | $0.017220 | 100 | 92 | execution-quality composite |
| Codex | PASS | 100.380s | 252,306 | $0.431287 | 100 | 90 | execution-quality composite |
| agy | FAIL | 47.220s | n/a | n/a | 0 | 29 | execution-quality composite |
