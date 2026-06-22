# BB-004 — Markdown table normalizer metrics

## Scope

- Type: Text processing
- Difficulty: L1
- Pass count: 6/6
- Execution score: deterministic composite from correctness, red-baseline capture, smoke evidence, independent verification, exit code, telemetry coverage, scenario-local speed percentile, and scenario-local token-efficiency percentile.

## Agent metrics

| Agent | Verdict | Wall | Tokens | Normalized public cost | Patch | Execution score | Notes |
|---|---:|---:|---:|---:|---:|---:|---|
| OpenCode | PASS | 167.030s | 103,515 | $0.062082 | 100 | 92 | execution-quality composite |
| Claude | PASS | 169.013s | 169,366 | $0.085769 | 100 | 88 | execution-quality composite |
| MiMo | PASS | 190.220s | 227,270 | $0.094997 | 100 | 82 | execution-quality composite |
| Pi | PASS | 247.114s | 62,200 | $0.059673 | 100 | 85 | execution-quality composite |
| Codex | PASS | 219.382s | 327,859 | $0.757551 | 100 | 73 | execution-quality composite |
| agy | PASS | 113.300s | n/a | n/a | 100 | 84 | execution-quality composite |
