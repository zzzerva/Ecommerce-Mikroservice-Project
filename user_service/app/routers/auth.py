from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.dependencies import require_role
from app.auth import create_access_token, verify_password, oauth2_scheme, TOKEN_BLACKLIST, get_current_user

router = APIRouter()

@router.post("/login")
async def login(user_data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == user_data.username).first()
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=schemas.ErrorMessages.INVALID_CREDENTIALS,
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data={"sub": str(user.id), "role": user.role}
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/protected-route")
async def protected_route(
    token: str = Depends(oauth2_scheme), 
    current_user: models.User = Depends(get_current_user)
):
    if token in TOKEN_BLACKLIST:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"message": f"Hello, {current_user.username}!"}

@router.get("/check-login")
async def check_login(token: str = Depends(oauth2_scheme)):
    from jose import JWTError, jwt
    from app.auth import SECRET_KEY, ALGORITHM
    try:
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if token in TOKEN_BLACKLIST:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"status": "Valid"}

@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    TOKEN_BLACKLIST.add(token)
    return {"message": "Logout successful, token is invalidated"}

@router.get("/user-info")
async def get_user_info(current_user: models.User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "role": current_user.role,
        "email": current_user.email
    }

@router.get("/admin-dashboard")
async def admin_dashboard(current_user: models.User = Depends(get_current_user)):
    if current_user.role != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"message": "Welcome to the Admin Dashboard!"}