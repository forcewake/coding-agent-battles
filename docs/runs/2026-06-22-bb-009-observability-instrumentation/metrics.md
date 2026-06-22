# BB-009 — Observability instrumentation metrics

## Scope

- Type: Non-functional backend
- Difficulty: L3
- Pass count: 5/6
- Token/cost extraction: not yet normalized for this bulk run; fields remain `n/a` until a separate ccusage/fallback telemetry pass.

## Agent metrics

| Agent | Verdict | Wall | Tokens | Cost | Notes |
|---|---:|---:|---:|---:|---|
| OpenCode | PASS | 58.357s | n/a | n/a | Hermes-independent verify passed |
| Claude | PASS | 89.627s | n/a | n/a | Hermes-independent verify passed |
| MiMo | PASS | 91.989s | n/a | n/a | Hermes-independent verify passed |
| Pi | PASS | 68.880s | n/a | n/a | Hermes-independent verify passed |
| Codex | PASS | 100.717s | n/a | n/a | Hermes-independent verify passed |
| agy | FAIL | 43.784s | n/a | n/a | Agent exited but independent verify failed |
