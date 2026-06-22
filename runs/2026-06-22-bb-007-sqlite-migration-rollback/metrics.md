# BB-007 — SQLite migration with rollback metrics

## Scope

- Type: Data migration
- Difficulty: L2
- Pass count: 6/6
- Token/cost extraction: not yet normalized for this bulk run; fields remain `n/a` until a separate ccusage/fallback telemetry pass.

## Agent metrics

| Agent | Verdict | Wall | Tokens | Cost | Notes |
|---|---:|---:|---:|---:|---|
| OpenCode | PASS | 48.124s | n/a | n/a | Hermes-independent verify passed |
| Claude | PASS | 86.768s | n/a | n/a | Hermes-independent verify passed |
| MiMo | PASS | 82.405s | n/a | n/a | Hermes-independent verify passed |
| Pi | PASS | 137.179s | n/a | n/a | Hermes-independent verify passed |
| Codex | PASS | 122.860s | n/a | n/a | Hermes-independent verify passed |
| agy | PASS | 74.759s | n/a | n/a | Hermes-independent verify passed |
