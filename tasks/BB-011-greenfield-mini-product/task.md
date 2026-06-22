# BB-011 — Long-horizon greenfield mini-product

Build a tiny benchmark registry API from tests/spec.

## Requirements
- Provide `create_app()` in `bb011_miniproduct.app` returning a FastAPI app.
- `POST /scenarios` accepts `{id,name,level}` and stores it in memory.
- Duplicate id returns 409.
- `GET /scenarios` returns scenarios sorted by level then id.
- `GET /healthz` returns `{"status":"ok"}`.
- `python verify.py` must pass.
