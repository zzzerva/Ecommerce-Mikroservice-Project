import pytest
from fastapi import status

def test_add_item_to_cart(client, user_token_headers, test_product, test_cart):
    response = client.post(
        "/api/v1/cart/items/",
        headers=user_token_headers,
        json={
            "product_id": test_product["id"],
            "quantity": 2
        }
    )
    assert response.status_code == status.HTTP_200_OK, response.text
    data = response.json()
    assert data["product_id"] == test_product["id"]
    assert data["quantity"] == 2

def test_add_same_item_increases_quantity(client, user_token_headers, test_product, test_cart):
    client.post(
        "/api/v1/cart/items/",
        headers=user_token_headers,
        json={"product_id": test_product["id"], "quantity": 1}
    )
    response = client.post(
        "/api/v1/cart/items/",
        headers=user_token_headers,
        json={"product_id": test_product["id"], "quantity": 3}
    )
    assert response.status_code == status.HTTP_200_OK, response.text
    data = response.json()
    assert data["product_id"] == test_product["id"]
    assert data["quantity"] == 4

# 3. Sepetten ürün çıkarma
def test_remove_item_from_cart(client, user_token_headers, test_product, test_cart):
    # Önce ekle
    add_resp = client.post(
        "/api/v1/cart/items/",
        headers=user_token_headers,
        json={"product_id": test_product["id"], "quantity": 1}
    )
    item_id = add_resp.json()["id"]
    # Sonra sil
    response = client.delete(
        f"/api/v1/cart/items/{item_id}",
        headers=user_token_headers
    )
    assert response.status_code == status.HTTP_200_OK, response.text
    data = response.json()
    assert data["id"] == item_id

# 4. Sepeti listeleme
def test_list_cart(client, user_token_headers, test_product, test_cart):
    # Sepete ürün ekle
    client.post(
        "/api/v1/cart/items/",
        headers=user_token_headers,
        json={"product_id": test_product["id"], "quantity": 2}
    )
    response = client.get(
        "/api/v1/cart/",
        headers=user_token_headers
    )
    assert response.status_code == status.HTTP_200_OK, response.text
    data = response.json()
    assert "items" in data
    assert any(item["product_id"] == test_product["id"] for item in data["items"])

# 5. Sepeti temizleme
def test_clear_cart(client, user_token_headers, test_product, test_cart):
    # Sepete ürün ekle
    client.post(
        "/api/v1/cart/items/",
        headers=user_token_headers,
        json={"product_id": test_product["id"], "quantity": 2}
    )
    # Temizle
    response = client.delete(
        "/api/v1/cart/clear",
        headers=user_token_headers
    )
    assert response.status_code == status.HTTP_200_OK, response.text
    # Sepeti tekrar listele
    response = client.get(
        "/api/v1/cart/",
        headers=user_token_headers
    )
    assert response.status_code == status.HTTP_200_OK, response.text
    data = response.json()
    assert data["items"] == [] 