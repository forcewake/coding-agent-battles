# BB-005 — FastAPI auth middleware bug

Fix the auth dependency so `/admin` requires `Authorization: Bearer secret-token` while `/healthz` stays public.

## Requirements
- No token => `/admin` returns 401.
- Wrong token => `/admin` returns 403.
- Correct token => 200 with `{"status":"ok","scope":"admin"}`.
- `/healthz` remains 200 without auth.
- `python verify.py` must pass.
