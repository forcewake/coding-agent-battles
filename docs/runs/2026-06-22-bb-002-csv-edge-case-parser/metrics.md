# BB-002 — CSV edge-case parser metrics

## Scope

- Type: Library bugfix
- Difficulty: L0
- Pass count: 6/6
- Execution score: deterministic composite from correctness, red-baseline capture, smoke evidence, independent verification, exit code, telemetry coverage, scenario-local speed percentile, and scenario-local token-efficiency percentile.

## Agent metrics

| Agent | Verdict | Wall | Tokens | Normalized public cost | Patch | Execution score | Notes |
|---|---:|---:|---:|---:|---:|---:|---|
| OpenCode | PASS | 80.638s | 105,968 | $0.034981 | 100 | 99 | execution-quality composite |
| Claude | PASS | 93.744s | 158,158 | $0.079108 | 100 | 98 | execution-quality composite |
| MiMo | PASS | 66.505s | 212,952 | $0.075279 | 100 | 100 | execution-quality composite |
| Pi | PASS | 125.715s | 25,482 | $0.030214 | 100 | 96 | execution-quality composite |
| Codex | PASS | 101.812s | 163,324 | $0.387700 | 100 | 97 | execution-quality composite |
| agy | PASS | 202.767s | n/a | n/a | 100 | 90 | execution-quality composite |
