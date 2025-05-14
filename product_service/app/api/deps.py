from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.core.database import get_db

# Dummy User and UserRole for demonstration
class UserRole:
    ADMIN = "admin"
    USER = "user"

class User:
    def __init__(self, id: int, is_admin: bool = False):
        self.id = id
        self.is_admin = is_admin
        self.role = UserRole.ADMIN if is_admin else UserRole.USER

# Dummy current user dependency (replace with real JWT logic in production)
def get_current_user(request: Request):
    auth = request.headers.get("authorization", "")
    if not auth:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    if "admin-token" in auth:
        return User(id=1, is_admin=True)
    return User(id=2, is_admin=False)

def get_current_active_user(current_user: User = Depends(get_current_user)):
    return current_user

def get_current_active_admin(current_user: User = Depends(get_current_user)):
    if not getattr(current_user, "is_admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user 