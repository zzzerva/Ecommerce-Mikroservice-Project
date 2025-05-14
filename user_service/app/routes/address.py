from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.address_service import AddressService
from app.schemas.address import Address, AddressCreate, AddressUpdate
from app.routes.user import get_current_user
from app.schemas.user import User

router = APIRouter(prefix="/address", tags=["address"])

@router.get("/", response_model=List[Address])
def list_addresses(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    address_service = AddressService(db)
    return address_service.get_user_addresses(current_user.id, skip=skip, limit=limit)

@router.post("/", response_model=Address)
def create_address(
    address: AddressCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    address_service = AddressService(db)
    return address_service.create_address(current_user.id, address)

@router.get("/{address_id}", response_model=Address)
def read_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    address_service = AddressService(db)
    address = address_service.get_address(address_id)
    if address.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return address

@router.put("/{address_id}", response_model=Address)
def update_address(
    address_id: int,
    address: AddressUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    address_service = AddressService(db)
    db_address = address_service.get_address(address_id)
    if db_address.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return address_service.update_address(address_id, address)

@router.delete("/{address_id}")
def delete_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    address_service = AddressService(db)
    db_address = address_service.get_address(address_id)
    if db_address.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return address_service.delete_address(address_id) 