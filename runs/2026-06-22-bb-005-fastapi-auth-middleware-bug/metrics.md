# BB-005 — FastAPI auth middleware bug metrics

## Scope

- Type: Backend debugging
- Difficulty: L2
- Pass count: 5/6
- Token/cost extraction: not yet normalized for this bulk run; fields remain `n/a` until a separate ccusage/fallback telemetry pass.

## Agent metrics

| Agent | Verdict | Wall | Tokens | Cost | Notes |
|---|---:|---:|---:|---:|---|
| OpenCode | PASS | 43.633s | n/a | n/a | Hermes-independent verify passed |
| Claude | PASS | 47.969s | n/a | n/a | Hermes-independent verify passed |
| MiMo | PASS | 46.894s | n/a | n/a | Hermes-independent verify passed |
| Pi | PASS | 87.805s | n/a | n/a | Hermes-independent verify passed |
| Codex | PASS | 100.380s | n/a | n/a | Hermes-independent verify passed |
| agy | FAIL | 47.220s | n/a | n/a | Agent exited but independent verify failed |
