# BB-009 — Observability instrumentation

Add request logging middleware with safe structured logs.

## Requirements
- Every request appends one JSON line to `app.state.events`.
- Event fields: `method`, `path`, `status_code`, `duration_ms`, `correlation_id`.
- Use incoming `x-correlation-id` when present; otherwise generate a non-empty id.
- Do not log authorization headers or request bodies.
- `python verify.py` must pass.
