from fastapi.testclient import TestClient
from apps.auth_service.main import app

def test_reproduce_crash():
    client = TestClient(app, raise_server_exceptions=False)
    response = client.get("/profile/999")
    assert response.status_code != 500