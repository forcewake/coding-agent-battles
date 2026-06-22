from fastapi.testclient import TestClient
from bb009_observe.app import app

def test_structured_request_event_without_secrets():
    app.state.events.clear()
    c = TestClient(app)
    r = c.get('/items/42', headers={'x-correlation-id': 'corr-123', 'authorization': 'Bearer SECRET'})
    assert r.status_code == 200
    assert len(app.state.events) == 1
    event = app.state.events[0]
    assert event['method'] == 'GET'
    assert event['path'] == '/items/42'
    assert event['status_code'] == 200
    assert event['correlation_id'] == 'corr-123'
    assert isinstance(event['duration_ms'], (int, float)) and event['duration_ms'] >= 0
    assert 'authorization' not in event and 'SECRET' not in repr(event)

def test_generates_correlation_id():
    app.state.events.clear()
    c = TestClient(app)
    c.get('/items/99')
    assert app.state.events[0]['correlation_id']
