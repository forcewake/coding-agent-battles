import time
import uuid

from fastapi import FastAPI, Request

app = FastAPI()
app.state.events = []


@app.middleware('http')
async def request_logging_middleware(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - start) * 1000
    correlation_id = request.headers.get('x-correlation-id') or uuid.uuid4().hex
    # Only the fields below are recorded; headers (e.g. authorization)
    # and request bodies are intentionally never logged.
    app.state.events.append({
        'method': request.method,
        'path': request.url.path,
        'status_code': response.status_code,
        'duration_ms': duration_ms,
        'correlation_id': correlation_id,
    })
    return response


@app.get('/items/{item_id}')
def get_item(item_id: str):
    return {'item_id': item_id}
