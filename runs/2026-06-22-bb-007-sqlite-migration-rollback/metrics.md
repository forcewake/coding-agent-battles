# BB-007 — SQLite migration with rollback metrics

## Scope

- Type: Data migration
- Difficulty: L2
- Pass count: 6/6
- Execution score: deterministic composite from correctness, red-baseline capture, smoke evidence, independent verification, exit code, telemetry coverage, scenario-local speed percentile, and scenario-local token-efficiency percentile.

## Agent metrics

| Agent | Verdict | Wall | Tokens | Normalized public cost | Patch | Execution score | Notes |
|---|---:|---:|---:|---:|---:|---:|---|
| OpenCode | PASS | 48.124s | 64,976 | $0.026777 | 100 | 98 | execution-quality composite |
| Claude | PASS | 86.768s | 183,359 | $0.088476 | 100 | 79 | execution-quality composite |
| MiMo | PASS | 82.405s | 191,087 | $0.059777 | 100 | 79 | execution-quality composite |
| Pi | PASS | 137.179s | 40,117 | $0.025923 | 100 | 85 | execution-quality composite |
| Codex | PASS | 122.860s | 176,231 | $0.418060 | 100 | 74 | execution-quality composite |
| agy | PASS | 74.759s | n/a | n/a | 100 | 79 | execution-quality composite |
