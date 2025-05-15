from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from .auth import SECRET_KEY, ALGORITHM, TOKEN_BLACKLIST
from .database import get_db
from . import models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if token in TOKEN_BLACKLIST:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception
    return user

def get_current_role(current_user: models.User = Depends(get_current_user)) -> str:
    if current_user.role not in ["User", "Admin"]:
        raise HTTPException(status_code=403, detail="Role geçersiz")
    return current_user.role

def require_role(required_roles: list):
    def role_checker(current_role: str = Depends(get_current_role)):
        if current_role not in required_roles:
            raise HTTPException(status_code=403, detail="Bu işlem için yetkiniz yok")
    return role_checker 