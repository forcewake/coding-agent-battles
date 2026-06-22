from fastapi.testclient import TestClient
from bb011_miniproduct.app import create_app

def test_scenario_registry_flow():
    client = TestClient(create_app())
    assert client.get('/healthz').json() == {'status': 'ok'}
    assert client.post('/scenarios', json={'id':'BB-011','name':'Mini product','level':4}).status_code == 201
    assert client.post('/scenarios', json={'id':'BB-002','name':'CSV','level':0}).status_code == 201
    assert client.post('/scenarios', json={'id':'BB-011','name':'Dup','level':4}).status_code == 409
    assert client.get('/scenarios').json() == [
      {'id':'BB-002','name':'CSV','level':0},
      {'id':'BB-011','name':'Mini product','level':4},
    ]
