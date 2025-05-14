import pytest
from fastapi import status

def test_create_contact_unauthorized(client, fake_contact_data):
    response = client.post("/api/v1/contact/", json=fake_contact_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_contacts_unauthorized(client):
    response = client.get("/api/v1/contact/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

