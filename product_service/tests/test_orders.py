import pytest
from fastapi import status
from app.models.order import Order, OrderItem, OrderStatus

def test_create_order(client, user_token_headers, test_product):
    response = client.post(
        "/api/v1/orders/",
        headers=user_token_headers,
        json={
            "user_id": 1,
            "shipping_address": "Test Address",
            "items": [
                {
                    "product_id": test_product["id"],
                    "quantity": 2
                }
            ]
        }
    )
    assert response.status_code == status.HTTP_200_OK, response.text
    data = response.json()
    assert data["shipping_address"] == "Test Address"
    assert data["status"] == OrderStatus.PENDING
    assert len(data["items"]) == 1
    assert data["items"][0]["product_id"] == test_product["id"]

def test_create_order_insufficient_stock(client, user_token_headers, test_product):
    response = client.post(
        "/api/v1/orders/",
        headers=user_token_headers,
        json={
            "user_id": 1,
            "shipping_address": "Test Address",
            "items": [
                {
                    "product_id": test_product["id"],
                    "quantity": test_product["stock"] + 1  # stoktan fazla gönderildi
                }
            ]
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.text  # veya sistem ne dönüyorsa

def test_create_order_from_cart(client, user_token_headers, test_cart, test_product):
    add_item_response = client.post(
        "/api/v1/cart/items/",
        headers=user_token_headers,
        json={
            "product_id": test_product["id"],
            "quantity": 1
        }
    )
    assert add_item_response.status_code == status.HTTP_200_OK, add_item_response.text

    response = client.post(
        "/api/v1/orders/from-cart/",
        headers=user_token_headers,
        params={"shipping_address": "Test Address"}  # query parametre olarak gönder
    )
    assert response.status_code == status.HTTP_200_OK, response.text
    data = response.json()
    assert data["shipping_address"] == "Test Address"
    assert data["status"] == OrderStatus.PENDING
    assert len(data["items"]) == 1
    assert data["items"][0]["product_id"] == test_product["id"]


def test_get_orders(client, user_token_headers):
    response = client.get(
        "/api/v1/orders/",
        headers=user_token_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)

def test_get_order(client, user_token_headers, test_product):
    # User ID eşleşmesini varsayıyoruz
    order_response = client.post(
        "/api/v1/orders/",
        headers=user_token_headers,
        json={
            "user_id": 2,  # kullanıcı token’ına gerçekten ait olmalı. 2 yapıyoruz çünkü 1 yaparsak test_product["id"] ile çakışır.
            "shipping_address": "Test Address",
            "items": [
                {
                    "product_id": test_product["id"],
                    "quantity": 1
                }
            ]
        }
    )
    assert order_response.status_code == status.HTTP_200_OK, order_response.text
    order = order_response.json()

    response = client.get(
        f"/api/v1/orders/{order['id']}",
        headers=user_token_headers
    )
    assert response.status_code == status.HTTP_200_OK, response.text
    data = response.json()
    assert data["id"] == order["id"]


def test_update_order_status(client, admin_token_headers, test_product):
    order = client.post(
        "/api/v1/orders/",
        headers=admin_token_headers,
        json={
            "user_id": 1,
            "shipping_address": "Test Address",
            "items": [
                {
                    "product_id": test_product["id"],
                    "quantity": 1
                }
            ]
        }
    ).json()

    response = client.put(
        f"/api/v1/orders/{order['id']}",
        headers=admin_token_headers,
        json={
            "status": OrderStatus.PROCESSING
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == OrderStatus.PROCESSING

def test_cancel_order(client, user_token_headers, test_product):
    order = client.post(
        "/api/v1/orders/",
        headers=user_token_headers,
        json={
            "user_id": 2,
            "shipping_address": "Test Address",
            "items": [
                {
                    "product_id": test_product["id"],
                    "quantity": 1
                }
            ]
        }
    ).json()

    response = client.post(
        f"/api/v1/orders/{order['id']}/cancel",
        headers=user_token_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == OrderStatus.CANCELLED

    product = client.get(
        f"/api/v1/products/{test_product['id']}"
    ).json()
    assert product["stock"] == test_product["stock"]  # Stock should be back to original 