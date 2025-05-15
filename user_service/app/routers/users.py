from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import re
from app import models, schemas
from app.database import get_db
from app.dependencies import require_role
from app.auth import get_current_user, get_password_hash, verify_password
from app.schemas import UserCreate, UserUpdate, PasswordChange, PasswordReset, UserStatus, AddressCreate, AddressUpdate, ContactCreate

router = APIRouter()

@router.post("/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )
    
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=schemas.ErrorMessages.USERNAME_EXISTS
        )
    
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=schemas.ErrorMessages.EMAIL_EXISTS
        )
    
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users/me", response_model=schemas.User)
async def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user

@router.get("/users/", response_model=List[schemas.User])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: str = Depends(require_role(["Admin"]))
):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

@router.get("/users/{user_id}", response_model=schemas.User)
async def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(require_role(["Admin"]))
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=404, 
            detail=schemas.ErrorMessages.USER_NOT_FOUND
        )
    return user

@router.put("/users/{user_id}", response_model=schemas.User)
async def update_user(
    user_id: int,
    user: schemas.UserUpdate,
    db: Session = Depends(get_db),
    _: str = Depends(require_role(["Admin"]))
):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(
            status_code=404, 
            detail=schemas.ErrorMessages.USER_NOT_FOUND
        )
    
    if user.username and user.username != db_user.username:
        existing_user = db.query(models.User).filter(models.User.username == user.username).first()
        if existing_user:
            raise HTTPException(
                status_code=400, 
                detail=schemas.ErrorMessages.USERNAME_EXISTS
            )
    
    if user.email and user.email != db_user.email:
        existing_user = db.query(models.User).filter(models.User.email == user.email).first()
        if existing_user:
            raise HTTPException(
                status_code=400, 
                detail=schemas.ErrorMessages.EMAIL_EXISTS
            )
    
    for key, value in user.model_dump(exclude_unset=True).items():
        if key == "password":
            value = get_password_hash(value)
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(require_role(["Admin"]))
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=404, 
            detail=schemas.ErrorMessages.USER_NOT_FOUND
        )
    
    db.delete(user)
    db.commit()
    return {"status": "success"}

@router.put("/users/me/password")
async def change_password(
    password_data: PasswordChange,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not verify_password(password_data.old_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect old password"
        )
    
    current_user.hashed_password = get_password_hash(password_data.new_password)
    db.commit()
    return {"message": "Password updated successfully"}

@router.put("/users/{user_id}/password/reset")
async def reset_user_password(
    user_id: int,
    password_data: PasswordReset,
    db: Session = Depends(get_db),
    _: str = Depends(require_role(["Admin"]))
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=schemas.ErrorMessages.USER_NOT_FOUND
        )
    
    user.hashed_password = get_password_hash(password_data.new_password)
    db.commit()
    return {"message": "Password reset successfully"}

@router.put("/users/{user_id}/status")
async def update_user_status(
    user_id: int,
    status_data: UserStatus,
    db: Session = Depends(get_db),
    _: str = Depends(require_role(["Admin"]))
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=schemas.ErrorMessages.USER_NOT_FOUND
        )
    
    user.is_active = status_data.is_active
    db.commit()
    return {"message": "User status updated successfully"}

@router.put("/users/me/deactivate")
async def deactivate_account(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    current_user.is_active = False
    db.commit()
    return {"message": "Account deactivated successfully"}

@router.post("/users/me/addresses", status_code=status.HTTP_201_CREATED)
async def add_address(
    address: AddressCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if address.type not in ["home", "work"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Address type must be either 'home' or 'work'"
        )
    
    db_address = models.Address(
        user_id=current_user.id,
        **address.model_dump()
    )
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address

@router.put("/users/me/addresses/{address_id}")
async def update_address(
    address_id: int,
    address_update: AddressUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_address = db.query(models.Address).filter(
        models.Address.id == address_id,
        models.Address.user_id == current_user.id
    ).first()
    
    if not db_address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found"
        )
    
    for key, value in address_update.model_dump(exclude_unset=True).items():
        setattr(db_address, key, value)
    
    db.commit()
    db.refresh(db_address)
    return db_address

@router.delete("/users/me/addresses/{address_id}")
async def delete_address(
    address_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_address = db.query(models.Address).filter(
        models.Address.id == address_id,
        models.Address.user_id == current_user.id
    ).first()
    
    if not db_address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found"
        )
    
    db.delete(db_address)
    db.commit()
    return {"message": "Address deleted successfully"}

@router.post("/users/me/contacts", status_code=status.HTTP_201_CREATED)
async def add_contact(
    contact: ContactCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not re.match(r"^\+?1?\d{9,15}$", contact.phone_number):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid phone number format"
        )
    
    db_contact = models.Contact(
        user_id=current_user.id,
        **contact.model_dump()
    )
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

@router.put("/users/{user_id}/role")
async def assign_role(
    user_id: int,
    role_data: dict,
    db: Session = Depends(get_db),
    _: str = Depends(require_role(["Admin"]))
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=schemas.ErrorMessages.USER_NOT_FOUND
        )
    
    role = db.query(models.Role).filter(models.Role.id == role_data["role_id"]).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
    
    user.role = role.name
    db.commit()
    return {"message": "Role assigned successfully"}
