import pytest
from fastapi import status

def test_login_wrong_username(client):
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "nonexistent", "password": "password"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_logout_unauthorized(client):
    response = client.post("/api/v1/auth/logout")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_check_login_invalid_token(client):
    response = client.get(
        "/api/v1/auth/checkLogin",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_check_login_no_token(client):
    response = client.get("/api/v1/auth/checkLogin")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED 