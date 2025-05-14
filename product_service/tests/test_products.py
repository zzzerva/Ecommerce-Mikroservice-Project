import pytest
from fastapi import status
from app.models.product import Product, Category

def test_create_category(client, admin_token_headers):
    response = client.post(
        "/api/v1/products/categories/",
        headers=admin_token_headers,
        json={"name": "New Category", "description": "New Description"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "New Category"
    assert data["description"] == "New Description"
    assert "id" in data

def test_create_category_duplicate_name(client, admin_token_headers, test_category):
    response = client.post(
        "/api/v1/products/categories/",
        headers=admin_token_headers,
        json={"name": test_category.name, "description": "Another Description"}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_create_category_unauthorized(client):
    response = client.post(
        "/api/v1/products/categories/",
        json={"name": "New Category", "description": "New Description"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_categories(client, test_category):
    response = client.get("/api/v1/products/categories/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert data[0]["name"] == test_category.name

def test_create_product(client, admin_token_headers, test_category):
    response = client.post(
        "/api/v1/products/",
        headers=admin_token_headers,
        json={
            "name": "New Product",
            "description": "New Description",
            "price": 99.99,
            "stock": 100,
            "category_id": test_category.id,
            "is_active": True
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "New Product"
    assert data["price"] == 99.99
    assert data["stock"] == 100
    assert data["category_id"] == test_category.id

def test_create_product_invalid_category(client, admin_token_headers):
    response = client.post(
        "/api/v1/products/",
        headers=admin_token_headers,
        json={
            "name": "New Product",
            "description": "New Description",
            "price": 99.99,
            "stock": 100,
            "category_id": 999,  # Non-existent category
            "is_active": True
        }
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_get_products(client, test_product):
    response = client.get("/api/v1/products/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) > 0
    assert data[0]["name"] == test_product["name"]

def test_get_product(client, test_product):
    response = client.get(f"/api/v1/products/{test_product['id']}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == test_product["id"]

def test_update_product(client, admin_token_headers, test_product):
    response = client.put(
        f"/api/v1/products/{test_product['id']}",
        headers=admin_token_headers,
        json={
            "name": "Updated Product",
            "price": 149.99,
            "stock": 50
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Updated Product"
    assert data["price"] == 149.99
    assert data["stock"] == 50

def test_delete_product(client, admin_token_headers, test_product):
    response = client.delete(
        f"/api/v1/products/{test_product['id']}",
        headers=admin_token_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == test_product["id"]
    
    # Verify product is deleted
    response = client.get(f"/api/v1/products/{test_product['id']}")
    assert response.status_code == status.HTTP_404_NOT_FOUND 
