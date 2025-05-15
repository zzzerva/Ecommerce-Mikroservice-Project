import os
import sys
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from datetime import datetime, timedelta, timezone
import jwt

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app
from app.database import Base, get_db
from app import models, schemas
from app.auth import get_password_hash, SECRET_KEY, ALGORITHM

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create test client
client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    
    # Create admin user
    admin_user = models.User(
        username="admin",
        email="admin@example.com",
        hashed_password=get_password_hash("admin123"),
        role="Admin"
    )
    
    # Create regular user
    regular_user = models.User(
        username="testuser",
        email="testuser@example.com",
        hashed_password=get_password_hash("password123"),
        role="User"
    )
    
    db.add(admin_user)
    db.add(regular_user)
    db.commit()
    db.close()
    
    yield
    
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def admin_token():
    response = client.post(
        "/login",
        json={"username": "admin", "password": "admin123"}
    )
    return response.json()["access_token"]

@pytest.fixture
def user_token():
    response = client.post(
        "/login",
        json={"username": "testuser", "password": "password123"}
    )
    return response.json()["access_token"]

# Authentication & Authorization Tests
def test_valid_login():
    """A1: Valid login credentials"""
    response = client.post(
        "/login",
        json={"username": "admin", "password": "admin123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_invalid_password_login():
    """A2: Invalid password login"""
    response = client.post(
        "/login",
        json={"username": "admin", "password": "wrongpassword"}
    )
    assert response.status_code == 401

def test_protected_route_unauthorized():
    """A3: Access protected route without login"""
    response = client.get("/protected-route")
    assert response.status_code == 401

def test_expired_token():
    """A4: Expired token check"""
    expired_token = jwt.encode(
        {
            "sub": "1",
            "role": "Admin",
            "exp": datetime.now(timezone.utc) - timedelta(minutes=1)
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    
    response = client.get(
        "/check-login",
        headers={"Authorization": f"Bearer {expired_token}"}
    )
    assert response.status_code == 401

def test_logout_invalidates_token(user_token):
    """A5: Token invalidation after logout"""
    response = client.get(
        "/protected-route",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 200
    
    response = client.post(
        "/logout",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 200
    
    response = client.get(
        "/protected-route",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 401

def test_get_user_info(user_token):
    """A6: Get user info with JWT token"""
    response = client.get(
        "/user-info",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_role_based_access(admin_token):
    """A7: Role-based access control"""
    response = client.get(
        "/admin-dashboard",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200

# User Management Tests
def test_admin_create_user(admin_token):
    """U1: Admin creates new user"""
    user_data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "Password123!",
        "role": "User"
    }
    response = client.post(
        "/users/",
        json=user_data,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 201
    assert response.json()["username"] == user_data["username"]

def test_duplicate_username(admin_token):
    """U2: Create user with existing username"""
    user_data = {
        "username": "testuser",
        "email": "new@example.com",
        "password": "Password123!",
        "role": "User"
    }
    response = client.post(
        "/users/",
        json=user_data,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 409

def test_change_password(user_token):
    """U3: User changes password with correct old password"""
    password_data = {
        "old_password": "password123",
        "new_password": "newpassword123"
    }
    response = client.put(
        "/users/me/password",
        json=password_data,
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 200

def test_change_password_wrong_old(user_token):
    """U4: User changes password with wrong old password"""
    password_data = {
        "old_password": "wrongpassword",
        "new_password": "newpassword123"
    }
    response = client.put(
        "/users/me/password",
        json=password_data,
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 400

def test_admin_reset_password(admin_token):
    """U5: Admin resets user password"""
    password_data = {
        "new_password": "newpassword123"
    }
    response = client.put(
        "/users/2/password/reset",
        json=password_data,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200

def test_update_user_status(admin_token):
    """U6: Update user status"""
    status_data = {
        "is_active": False
    }
    response = client.put(
        "/users/2/status",
        json=status_data,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200

def test_user_self_deactivate(user_token):
    """U7: User deactivates own account"""
    response = client.put(
        "/users/me/deactivate",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 200
    
def test_get_user_by_id(admin_token):
    """U8: Get user by valid ID"""
    response = client.get(
        "/users/2",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_get_nonexistent_user(admin_token):
    """U9: Get user with invalid ID"""
    response = client.get(
        "/users/999",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 404

# Contact & Address Tests
def test_add_user_address(user_token):
    """C1: Add new address"""
    address_data = {
        "type": "home",
        "street": "123 Main St",
        "city": "Test City",
        "state": "Test State",
        "country": "Test Country",
        "postal_code": "12345"
    }
    response = client.post(
        "/users/me/addresses",
        json=address_data,
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 201

def test_update_address(user_token):
    """C2: Update address"""
    address_data = {
        "type": "home",
        "street": "123 Main St",
        "city": "Test City",
        "state": "Test State",
        "country": "Test Country",
        "postal_code": "12345"
    }
    create_response = client.post(
        "/users/me/addresses",
        json=address_data,
        headers={"Authorization": f"Bearer {user_token}"}
    )
    address_id = create_response.json()["id"]
    
    update_data = {
        "street": "456 New St",
        "city": "New City"
    }
    response = client.put(
        f"/users/me/addresses/{address_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 200

def test_delete_invalid_address(user_token):
    """C3: Delete invalid address"""
    response = client.delete(
        "/users/me/addresses/999",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 404
    
def test_add_contact_info(user_token):
    """C4: Add contact information"""
    contact_data = {
        "phone_type": "home",
        "phone_number": "+1234567890"
    }
    response = client.post(
        "/users/me/contacts",
        json=contact_data,
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 201

def test_invalid_contact_format(user_token):
    """C5: Add invalid contact format"""
    contact_data = {
        "phone_type": "home",
        "phone_number": "invalid-phone"
    }
    response = client.post(
        "/users/me/contacts",
        json=contact_data,
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 400

#Role & Permission Test Senaryoları
def test_create_role(admin_token):
    """R1: Create new role"""
    role_data = {
        "name": "Editor",
        "permissions": ["read", "write"]
    }
    response = client.post(
        "/roles",
        json=role_data,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 201

def test_update_role(admin_token):
    """R2: Update role details"""
    role_data = {
        "name": "Editor",
        "permissions": ["read", "write"]
    }
    create_response = client.post(
        "/roles",
        json=role_data,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    role_id = create_response.json()["id"]
    
    update_data = {
        "permissions": ["read", "write", "delete"]
    }
    response = client.put(
        f"/roles/{role_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200

def test_assign_role(admin_token):
    """R3: Assign role to user"""
    user_data = {
        "username": "test1user",
        "email": "test1user@example.com",
        "password": "Password123!",
        "role": "User"
    }
    user_resp = client.post(
        "/users/",
        json=user_data,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    if user_resp.status_code == 201:
        user_id = user_resp.json()["id"]
    else:
        users = client.get(
            "/users/",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        user_id = [u["id"] for u in users.json() if u["username"] == "test1user"][0]

    role_data = {
        "name": "roletest",
        "permissions": []
    }
    role_resp = client.post(
        "/roles",
        json=role_data,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    if role_resp.status_code == 201:
        role_id = role_resp.json()["id"]
    else:
        role_id = 2

    assign_data = {"role_id": role_id}
    response = client.put(
        "/users/2/role",
        json=assign_data,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200

def test_assign_nonexistent_role(admin_token):
    """R4: Assign non-existent role"""
    role_data = {
        "role_id": 999 
    }
    response = client.put(
        "/users/2/role",
        json=role_data,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 404

def test_assign_permission(admin_token):
    """R5: Assign permission to role"""
    role_data = {
        "name": "TestRole",
        "permissions": []
    }
    role_resp = client.post(
        "/roles",
        json=role_data,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    if role_resp.status_code == 201:
        role_id = role_resp.json()["id"]
    else:
        role_id = 1

    permission_data = {
        "permission": "delete"
    }
    response = client.post(
        f"/roles/{role_id}/permissions",
        json=permission_data,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200

# Validation Tests
def test_short_password():
    """V1: Password too short"""
    user_data = {
        "username": "newuser",
        "email": "new@example.com",
        "password": "short",
        "role": "User"
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 422

def test_invalid_email():
    """V2: Invalid email format"""
    user_data = {
        "username": "newuser",
        "email": "invalid-email",
        "password": "password123",
        "role": "User"
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 422

def test_invalid_address_type(user_token):
    """V3: Invalid address type"""
    address_data = {
        "type": "invalid",
        "street": "123 Main St",
        "city": "Test City",
        "state": "Test State",
        "country": "Test Country",
        "postal_code": "12345"
    }
    response = client.post(
        "/users/me/addresses",
        json=address_data,
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 400

def test_invalid_phone_format(user_token):
    """V4: Invalid phone format"""
    contact_data = {
        "phone_type": "home",
        "phone_number": "123"
    }
    response = client.post(
        "/users/me/contacts",
        json=contact_data,
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 400

def test_missing_required_fields():
    """V5: Missing required fields"""
    user_data = {
        "username": "newuser"
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 422 