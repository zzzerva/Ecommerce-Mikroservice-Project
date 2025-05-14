import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.main import app
from app.core.config import settings

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Test database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# Create test engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def user_headers(normal_user):
    token = create_access_token(subject=str(normal_user.id))  # ID kullan
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture(scope="function")
def admin_headers(admin_user):
    token = create_access_token(subject=str(admin_user.id))  # ID kullan  
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture(scope="function")
def test_category(db):
    from app.models.product import Category
    category = Category(name="Test Category", description="Test Description")
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

@pytest.fixture(scope="function")
def test_product(db, test_category):
    from app.models.product import Product
    product = Product(
        name="Test Product",
        description="Test Description",
        price=100.0,
        stock=10,
        category_id=test_category.id,
        is_active=True
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "stock": product.stock,
        "category_id": product.category_id,
        "is_active": product.is_active
    }

@pytest.fixture(scope="function")
def test_cart(db):
    from app.models.cart import Cart
    cart = Cart(user_id=1)
    db.add(cart)
    db.commit()
    db.refresh(cart)
    return cart 