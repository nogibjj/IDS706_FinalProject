from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_index():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == "Welcome to my fast API"


test_index()
