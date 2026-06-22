# BB-011 — Greenfield mini-product metrics

## Scope

- Type: Greenfield product
- Difficulty: L4
- Pass count: 6/6
- Execution score: deterministic composite from correctness, red-baseline capture, smoke evidence, independent verification, clean agent exit, and scenario-local speed percentile. Token/cost telemetry is reported separately and is not part of execution quality.

## Agent metrics

| Agent | Verdict | Wall | Tokens | Normalized public cost | Patch | Execution score | Notes |
|---|---:|---:|---:|---:|---:|---:|---|
| OpenCode | PASS | 47.141s | 53,112 | $0.020773 | 100 | 100 | execution-quality composite |
| Claude | PASS | 95.167s | 177,821 | $0.056421 | 100 | 91 | execution-quality composite |
| MiMo | PASS | 49.366s | 190,265 | $0.058130 | 100 | 100 | execution-quality composite |
| Pi | PASS | 71.199s | 30,285 | $0.012942 | 100 | 96 | execution-quality composite |
| Codex | PASS | 101.535s | 204,368 | $0.438527 | 100 | 90 | execution-quality composite |
| agy | PASS | 50.500s | n/a | n/a | 100 | 99 | execution-quality composite |
