from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.address import Address
from app.repository.address_repository import AddressRepository
from app.schemas.address import AddressCreate, AddressUpdate
from app.services.user_service import UserService

class AddressService:
    def __init__(self, db: Session):
        self.db = db
        self.address_repository = AddressRepository(db)
        self.user_service = UserService(db)

    def get_address(self, address_id: int) -> Address:
        address = self.address_repository.get_by_id(address_id)
        if not address:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Address not found"
            )
        return address

    def get_user_addresses(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Address]:
        self.user_service.get_user(user_id) 
        return self.address_repository.get_by_user_id(user_id, skip=skip, limit=limit)

    def create_address(self, user_id: int, address: AddressCreate) -> Address:
        self.user_service.get_user(user_id) 
        return self.address_repository.create(user_id, address)

    def update_address(self, address_id: int, address: AddressUpdate) -> Address:
        db_address = self.get_address(address_id)
        updated_address = self.address_repository.update(address_id, address)
        if not updated_address:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Address not found"
            )
        return updated_address

    def delete_address(self, address_id: int) -> bool:
        self.get_address(address_id)  
        return self.address_repository.delete(address_id) 