from fastapi.testclient import TestClient
from bb005_authapi.app import app

client = TestClient(app)

def test_healthz_public():
    assert client.get('/healthz').status_code == 200

def test_admin_requires_token():
    assert client.get('/admin').status_code == 401
    assert client.get('/admin', headers={'Authorization': 'Bearer wrong'}).status_code == 403
    r = client.get('/admin', headers={'Authorization': 'Bearer secret-token'})
    assert r.status_code == 200
    assert r.json() == {'status': 'ok', 'scope': 'admin'}
