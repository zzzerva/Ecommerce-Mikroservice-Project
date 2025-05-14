import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Set testing environment
os.environ["TESTING"] = "1"

from app.core.database import Base, get_db
from app.main import app
from app.core.security import create_access_token
from app.models.user import User
from app.models.address import Address
from app.models.contact import Contact
from faker import Faker

fake = Faker()

# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def prepare_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture(scope="function")
def client(db_session, monkeypatch):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

@pytest.fixture(scope="function")
def admin_user(db_session):
    user = User(
        email="admin@example.com",
        username="admin",
        hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "password"
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture(scope="function")
def normal_user(db_session):
    user = User(
        email="user@example.com",
        username="user",
        hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "password"
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture(scope="function")
def admin_headers(admin_user):
    token = create_access_token(subject=admin_user.email)
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture(scope="function")
def user_headers(normal_user):
    token = create_access_token(subject=normal_user.email)
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture(scope="function")
def fake_user_data():
    return {
        "email": fake.email(),
        "username": fake.user_name(),
        "password": "testpassword",
        "full_name": fake.name()
    }

@pytest.fixture(scope="function")
def fake_address(db_session, normal_user):
    address = Address(
        user_id=normal_user.id,
        street=fake.street_address(),
        city=fake.city(),
        state=fake.state(),
        country=fake.country(),
        postal_code=fake.postcode()
    )
    db_session.add(address)
    db_session.commit()
    db_session.refresh(address)
    return address

@pytest.fixture(scope="function")
def fake_address_data():
    return {
        "type": "home",
        "street": fake.street_address(),
        "city": fake.city(),
        "state": fake.state(),
        "country": fake.country(),
        "postal_code": fake.postcode()
    }

@pytest.fixture(scope="function")
def fake_contact(db_session, normal_user):
    contact = Contact(
        user_id=normal_user.id,
        phone=fake.phone_number(),
        email=fake.email(),
        type="personal"
    )
    db_session.add(contact)
    db_session.commit()
    db_session.refresh(contact)
    return contact

@pytest.fixture(scope="function")
def fake_contact_data():
    return {
        "phone": fake.phone_number(),
        "email": fake.email(),
        "type": "work"
    } 