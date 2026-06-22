# BB-001 — Broken CLI argument metrics

## Scope

- Type: CLI bugfix
- Difficulty: L0
- Pass count: 6/6
- Execution score: deterministic composite from correctness, red-baseline capture, smoke evidence, independent verification, clean agent exit, and scenario-local speed percentile. Token/cost telemetry is reported separately and is not part of execution quality.

## Agent metrics

| Agent | Verdict | Wall | Tokens | Normalized public cost | Patch | Execution score | Notes |
|---|---:|---:|---:|---:|---:|---:|---|
| OpenCode | PASS | 94.645s | 195,887 | $0.065351 | 100 | 96 | execution-quality composite |
| Claude | PASS | 53.025s | 208,020 | $0.066573 | 100 | 100 | execution-quality composite |
| MiMo | PASS | 64.559s | 262,659 | $0.088933 | 100 | 99 | execution-quality composite |
| Pi | PASS | 119.437s | 69,756 | $0.032009 | 100 | 93 | execution-quality composite |
| Codex | PASS | 147.902s | 455,504 | $0.644985 | 100 | 90 | execution-quality composite |
| agy | PASS | 51.705s | n/a | n/a | 100 | 100 | execution-quality composite |
