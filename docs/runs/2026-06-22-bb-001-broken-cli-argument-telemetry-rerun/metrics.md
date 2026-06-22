# BB-001 — Broken CLI argument metrics

## Scope

- Type: CLI bugfix
- Difficulty: L0
- Pass count: 6/6
- Execution score: deterministic composite from correctness, red-baseline capture, smoke evidence, independent verification, exit code, telemetry coverage, scenario-local speed percentile, and scenario-local token-efficiency percentile.

## Agent metrics

| Agent | Verdict | Wall | Tokens | Normalized public cost | Patch | Execution score | Notes |
|---|---:|---:|---:|---:|---:|---:|---|
| OpenCode | PASS | 35.587s | 63,995 | $0.025004 | 100 | 73 | execution-quality composite |
| Claude | PASS | 40.680s | 126,008 | $0.043040 | 100 | 59 | execution-quality composite |
| MiMo | PASS | 63.621s | 128,610 | $0.063052 | 100 | 57 | execution-quality composite |
| Pi | PASS | 70.733s | 25,910 | $0.015809 | 100 | 82 | execution-quality composite |
| Codex | PASS | 114.752s | 318,536 | $0.509121 | 100 | 52 | execution-quality composite |
| agy | PASS | 191.826s | n/a | n/a | 100 | 44 | execution-quality composite |
