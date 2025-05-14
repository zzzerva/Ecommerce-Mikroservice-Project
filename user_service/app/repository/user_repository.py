from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash
from typing import List, Optional

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def get_by_username(self, username: str) -> Optional[User]:
        return self.db.query(User).filter(User.username == username).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        return self.db.query(User).offset(skip).limit(limit).all()

    def create(self, user: UserCreate) -> User:
        db_user = User(
            email=user.email,
            username=user.username,
            hashed_password=get_password_hash(user.password),
            full_name=user.full_name,
            role=user.role
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update(self, user_id: int, user: UserUpdate) -> Optional[User]:
        db_user = self.get_by_id(user_id)
        if not db_user:
            return None

        update_data = user.dict(exclude_unset=True)
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

        for field, value in update_data.items():
            setattr(db_user, field, value)

        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def delete(self, user_id: int) -> bool:
        db_user = self.get_by_id(user_id)
        if not db_user:
            return False
        db_user.is_deleted = True
        self.db.commit()
        return True

    def deactivate(self, user_id: int) -> bool:
        db_user = self.get_by_id(user_id)
        if not db_user:
            return False
        db_user.is_active = False
        self.db.commit()
        return True 