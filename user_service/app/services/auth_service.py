from datetime import timedelta
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.core.security import verify_password, create_access_token
from app.repository.user_repository import UserRepository
from app.core.config import settings
import jwt
from jwt import PyJWTError

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)

    def authenticate(self, username: str, password: str) -> Optional[str]:
        user = self.user_repository.get_by_username(username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )
        return create_access_token(
            subject=user.id,
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )

    def validate_token(self, token: str) -> Optional[int]:
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            user_email: str = payload.get("sub")
            if user_email is None:
                return None
            
            # Email ile kullanıcıyı bul ve ID'sini döndür
            from app.services.user_service import UserService
            user_service = UserService(db_session=self.db)  # DB session'ı inject etmeniz gerekir
            user = user_service.get_user_by_email(user_email)
            return user.id if user else None
            
        except PyJWTError:
            return None 