# BB-003 — JSON export for existing CLI metrics

## Scope

- Type: CLI feature
- Difficulty: L1
- Pass count: 6/6
- Execution score: deterministic composite from correctness, red-baseline capture, smoke evidence, independent verification, clean agent exit, and scenario-local speed percentile. Token/cost telemetry is reported separately and is not part of execution quality.

## Agent metrics

| Agent | Verdict | Wall | Tokens | Normalized public cost | Patch | Execution score | Notes |
|---|---:|---:|---:|---:|---:|---:|---|
| OpenCode | PASS | 69.014s | 149,410 | $0.051976 | 100 | 94 | execution-quality composite |
| Claude | PASS | 80.125s | 164,894 | $0.062663 | 100 | 93 | execution-quality composite |
| MiMo | PASS | 63.405s | 159,098 | $0.054476 | 100 | 95 | execution-quality composite |
| Pi | PASS | 94.955s | 50,657 | $0.030755 | 100 | 91 | execution-quality composite |
| Codex | PASS | 103.024s | 187,021 | $0.395188 | 100 | 90 | execution-quality composite |
| agy | PASS | 19.505s | n/a | n/a | 100 | 100 | execution-quality composite |
