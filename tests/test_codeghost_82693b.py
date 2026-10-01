from fastapi.testclient import TestClient
from main import app

def test_reproduce_crash():
    client = TestClient(app, raise_server_exceptions=False)
    response = client.get("/rooms/huddle-0/occupancy")
    assert response.status_code != 500