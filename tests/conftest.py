import pytest
from app.core.security import create_access_token

@pytest.fixture(scope="function")
def admin_headers(admin_user):
    token = create_access_token(subject=str(admin_user.id))
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture(scope="function")
def user_headers(normal_user):
    token = create_access_token(subject=str(normal_user.id))
    return {"Authorization": f"Bearer {token}"} 