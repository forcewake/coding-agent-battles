# BB-010 — DOCX extraction quality fix metrics

## Scope

- Type: Document extraction
- Difficulty: L3
- Pass count: 6/6
- Token/cost extraction: not yet normalized for this bulk run; fields remain `n/a` until a separate ccusage/fallback telemetry pass.

## Agent metrics

| Agent | Verdict | Wall | Tokens | Cost | Notes |
|---|---:|---:|---:|---:|---|
| OpenCode | PASS | 67.775s | n/a | n/a | Hermes-independent verify passed |
| Claude | PASS | 69.886s | n/a | n/a | Hermes-independent verify passed |
| MiMo | PASS | 336.866s | n/a | n/a | Hermes-independent verify passed |
| Pi | PASS | 79.757s | n/a | n/a | Hermes-independent verify passed |
| Codex | PASS | 129.014s | n/a | n/a | Hermes-independent verify passed |
| agy | PASS | 103.864s | n/a | n/a | Hermes-independent verify passed |
