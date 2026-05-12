import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def get_token() -> str:
    response = client.post(
        "/token",
        data={"username": "admin", "password": "admin123"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


class TestTokenEndpoint:
    def test_login_success(self):
        response = client.post(
            "/token",
            data={"username": "admin", "password": "admin123"},
        )
        assert response.status_code == 200
        body = response.json()
        assert "access_token" in body
        assert body["token_type"] == "bearer"
        assert body["expires_in"] == 300

    def test_login_wrong_password(self):
        response = client.post(
            "/token",
            data={"username": "admin", "password": "wrong"},
        )
        assert response.status_code == 401

    def test_login_unknown_user(self):
        response = client.post(
            "/token",
            data={"username": "unknown", "password": "admin123"},
        )
        assert response.status_code == 401


class TestRefreshEndpoint:
    def test_refresh_valid_token(self):
        token = get_token()
        response = client.post("/token/refresh", json={"token": token})
        assert response.status_code == 200
        body = response.json()
        assert "access_token" in body
        assert body["expires_in"] == 300

    def test_refresh_invalid_token(self):
        response = client.post("/token/refresh", json={"token": "not.a.valid.token"})
        assert response.status_code == 401


class TestMeEndpoint:
    def test_me_authenticated(self):
        token = get_token()
        response = client.get("/me", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        assert response.json()["username"] == "admin"

    def test_me_unauthenticated(self):
        response = client.get("/me")
        assert response.status_code == 401

    def test_me_invalid_token(self):
        response = client.get("/me", headers={"Authorization": "Bearer invalid.token"})
        assert response.status_code == 401
