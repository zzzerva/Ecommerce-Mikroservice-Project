import pytest
from fastapi import status

def test_list_users_unauthorized(client):
    response = client.get("/api/v1/user/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_current_user_unauthorized(client):
    response = client.get("/api/v1/user/me")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_user_forbidden(client, user_headers, normal_user):
    response = client.get(f"/api/v1/user/{normal_user.id}", headers=user_headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_create_user_unauthorized(client, fake_user_data):
    response = client.post("/api/v1/user/", json=fake_user_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


