from fastapi.testclient import TestClient

from database import Base, engine
from main import app

client = TestClient(app)


def setup_function():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def auth_headers(email: str = "owner@example.com") -> dict[str, str]:
    client.post("/api/auth/register", json={"email": email, "password": "password123"})
    response = client.post("/api/auth/login", data={"username": email, "password": "password123"})
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def test_registration_login_and_duplicate_protection():
    response = client.post("/api/auth/register", json={"email": "user@example.com", "password": "password123"})
    assert response.status_code == 201
    assert "password_hash" not in response.json()
    assert client.post("/api/auth/register", json={"email": "user@example.com", "password": "password123"}).status_code == 409
    assert client.post("/api/auth/login", data={"username": "user@example.com", "password": "wrongpass"}).status_code == 401


def test_idea_crud_search_filter_and_ownership():
    headers = auth_headers()
    created = client.post(
        "/api/ideas",
        headers=headers,
        json={"title": "Build a garden app", "description": "Small", "tags": ["garden"], "status": "Inbox"},
    )
    assert created.status_code == 201
    idea_id = created.json()["id"]
    assert len(client.get("/api/ideas?search=garden&tag=garden", headers=headers).json()) == 1
    assert client.put(
        f"/api/ideas/{idea_id}",
        headers=headers,
        json={"title": "Build a garden app", "description": None, "tags": ["garden"], "status": "Completed"},
    ).json()["status"] == "Completed"
    other_headers = auth_headers("other@example.com")
    assert client.get(f"/api/ideas/{idea_id}", headers=other_headers).status_code == 404
    assert client.delete(f"/api/ideas/{idea_id}", headers=headers).status_code == 204
