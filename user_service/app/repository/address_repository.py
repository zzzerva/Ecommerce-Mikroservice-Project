from sqlalchemy.orm import Session
from app.models.address import Address
from app.schemas.address import AddressCreate, AddressUpdate
from typing import List, Optional

class AddressRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, address_id: int) -> Optional[Address]:
        return self.db.query(Address).filter(Address.id == address_id).first()

    def get_by_user_id(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Address]:
        return self.db.query(Address).filter(Address.user_id == user_id).offset(skip).limit(limit).all()

    def create(self, user_id: int, address: AddressCreate) -> Address:
        db_address = Address(**address.model_dump(), user_id=user_id)
        self.db.add(db_address)
        self.db.commit()
        self.db.refresh(db_address)
        return db_address

    def update(self, address_id: int, address: AddressUpdate) -> Optional[Address]:
        db_address = self.get_by_id(address_id)
        if not db_address:
            return None

        update_data = address.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_address, field, value)

        self.db.commit()
        self.db.refresh(db_address)
        return db_address

    def delete(self, address_id: int) -> bool:
        db_address = self.get_by_id(address_id)
        if not db_address:
            return False
        self.db.delete(db_address)
        self.db.commit()
        return True 