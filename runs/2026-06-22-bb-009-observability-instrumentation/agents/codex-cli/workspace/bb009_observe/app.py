import time
import uuid

from fastapi import FastAPI

app = FastAPI()
app.state.events = []

@app.middleware("http")
async def log_request(request, call_next):
    start = time.perf_counter()
    correlation_id = request.headers.get("x-correlation-id") or uuid.uuid4().hex
    status_code = 500
    try:
        response = await call_next(request)
        status_code = response.status_code
        return response
    finally:
        app.state.events.append({
            "method": request.method,
            "path": request.url.path,
            "status_code": status_code,
            "duration_ms": (time.perf_counter() - start) * 1000,
            "correlation_id": correlation_id,
        })

@app.get('/items/{item_id}')
def get_item(item_id: str):
    return {'item_id': item_id}
