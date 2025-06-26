from fastapi.testclient import TestClient
from main import app


def test_app_import():
    client = TestClient(app)
    response = client.get("/docs")
    assert response.status_code == 200
