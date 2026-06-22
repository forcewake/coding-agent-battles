# BB-002 — CSV edge-case parser metrics

## Scope

- Type: Library bugfix
- Difficulty: L0
- Pass count: 6/6
- Token/cost extraction: not yet normalized for this bulk run; fields remain `n/a` until a separate ccusage/fallback telemetry pass.

## Agent metrics

| Agent | Verdict | Wall | Tokens | Cost | Notes |
|---|---:|---:|---:|---:|---|
| OpenCode | PASS | 80.638s | n/a | n/a | Hermes-independent verify passed |
| Claude | PASS | 93.744s | n/a | n/a | Hermes-independent verify passed |
| MiMo | PASS | 66.505s | n/a | n/a | Hermes-independent verify passed |
| Pi | PASS | 125.715s | n/a | n/a | Hermes-independent verify passed |
| Codex | PASS | 101.812s | n/a | n/a | Hermes-independent verify passed |
| agy | PASS | 202.767s | n/a | n/a | Hermes-independent verify passed |
