import pytest
from fastapi import status



def test_create_address_unauthorized(client, fake_address_data):
    response = client.post("/api/v1/address/", json=fake_address_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_addresses_unauthorized(client):
    response = client.get("/api/v1/address/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

