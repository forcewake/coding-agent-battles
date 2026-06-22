# BB-007 — SQLite migration with rollback

Fix migration rollback safety.

## Requirements
- `upgrade(conn)` adds nullable `email` column to `users` and preserves rows.
- `downgrade(conn)` removes the `email` column and preserves `id/name` rows.
- Running upgrade twice must not duplicate/fail.
- `python verify.py` must pass.
