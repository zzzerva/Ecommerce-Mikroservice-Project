from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.user_service import UserService
from app.services.auth_service import AuthService
from app.schemas.user import User, UserCreate, UserUpdate
from app.routes.auth import oauth2_scheme
from app.models.user import UserRole

router = APIRouter(prefix="/user", tags=["user"])

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    auth_service = AuthService(db)
    user_service = UserService(db)
    user_id = auth_service.validate_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_service.get_user(user_id)

def get_current_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user

@router.get("/", response_model=List[User])
def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    user_service = UserService(db)
    return user_service.get_users(skip=skip, limit=limit)

@router.get("/me", response_model=User)
def read_user_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/{user_id}", response_model=User)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    user_service = UserService(db)
    return user_service.get_user(user_id)

@router.post("/", response_model=User)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    user_service = UserService(db)
    return user_service.create_user(user)

@router.put("/{user_id}", response_model=User)
def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.id != user_id and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    user_service = UserService(db)
    return user_service.update_user(user_id, user)

@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    user_service = UserService(db)
    return user_service.delete_user(user_id)

@router.patch("/deactivate")
def deactivate_self(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_service = UserService(db)
    return user_service.deactivate_user(current_user.id)

@router.patch("/deactivate/{user_id}")
def deactivate_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    user_service = UserService(db)
    return user_service.deactivate_user(user_id)

@router.patch("/reset-password/{user_id}")
def reset_password(
    user_id: int,
    new_password: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    user_service = UserService(db)
    return user_service.reset_password(user_id, new_password)

@router.patch("/change-password")
def change_password(
    current_password: str,
    new_password: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_service = UserService(db)
    return user_service.change_password(current_user.id, current_password, new_password) 