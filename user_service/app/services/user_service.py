from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User, UserRole
from app.repository.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password

class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)

    def get_user(self, user_id: int) -> Optional[User]:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user

    def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        return self.user_repository.get_all(skip=skip, limit=limit)

    def create_user(self, user: UserCreate) -> User:
        db_user = self.user_repository.get_by_email(user.email)
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        db_user = self.user_repository.get_by_username(user.username)
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        return self.user_repository.create(user)

    def update_user(self, user_id: int, user: UserUpdate) -> User:
        db_user = self.get_user(user_id)
        if user.email and user.email != db_user.email:
            if self.user_repository.get_by_email(user.email):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
        if user.username and user.username != db_user.username:
            if self.user_repository.get_by_username(user.username):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already taken"
                )
        return self.user_repository.update(user_id, user)

    def delete_user(self, user_id: int) -> bool:
        return self.user_repository.delete(user_id)

    def deactivate_user(self, user_id: int) -> bool:
        return self.user_repository.deactivate(user_id)

    def change_password(self, user_id: int, current_password: str, new_password: str) -> bool:
        user = self.get_user(user_id)
        if not verify_password(current_password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect password"
            )
        user.hashed_password = get_password_hash(new_password)
        self.db.commit()
        return True

    def reset_password(self, user_id: int, new_password: str) -> bool:
        user = self.get_user(user_id)
        user.hashed_password = get_password_hash(new_password)
        self.db.commit()
        return True 