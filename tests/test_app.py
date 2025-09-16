import pytest

import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_hello_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert "message" in data
    assert data["message"] == "Hello from Flask API!"


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"


def test_get_users(client):
    response = client.get("/api/users")
    assert response.status_code == 200
    data = response.get_json()
    assert "users" in data
    assert len(data["users"]) == 2


def test_create_user_valid(client):
    user_data = {"name": "Charlie", "email": "charlie@example.com"}
    response = client.post("/api/users", json=user_data)
    assert response.status_code == 201
    data = response.get_json()
    assert data["user"]["name"] == "Charlie"


def test_create_user_invalid(client):
    response = client.post("/api/users", json={})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
