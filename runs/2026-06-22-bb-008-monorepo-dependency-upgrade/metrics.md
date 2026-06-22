# BB-008 — Monorepo dependency upgrade metrics

## Scope

- Type: Tooling / monorepo
- Difficulty: L3
- Pass count: 6/6
- Execution score: deterministic composite from correctness, red-baseline capture, smoke evidence, independent verification, clean agent exit, and scenario-local speed percentile. Token/cost telemetry is reported separately and is not part of execution quality.

## Agent metrics

| Agent | Verdict | Wall | Tokens | Normalized public cost | Patch | Execution score | Notes |
|---|---:|---:|---:|---:|---:|---:|---|
| OpenCode | PASS | 42.590s | 86,204 | $0.035012 | 100 | 98 | execution-quality composite |
| Claude | PASS | 34.085s | 124,808 | $0.060092 | 100 | 100 | execution-quality composite |
| MiMo | PASS | 42.267s | 187,931 | $0.055319 | 100 | 98 | execution-quality composite |
| Pi | PASS | 54.993s | 22,078 | $0.011694 | 100 | 96 | execution-quality composite |
| Codex | PASS | 82.653s | 233,649 | $0.383047 | 100 | 90 | execution-quality composite |
| agy | PASS | 34.446s | n/a | n/a | 100 | 100 | execution-quality composite |
