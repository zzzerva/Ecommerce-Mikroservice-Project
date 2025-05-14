from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.address import AddressType

class AddressBase(BaseModel):
    type: str
    street: str
    city: str
    state: str
    country: str
    postal_code: str
    is_default: bool = False

class AddressCreate(AddressBase):
    pass

class AddressUpdate(BaseModel):
    type: Optional[AddressType] = None
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    is_default: Optional[bool] = None

class AddressInDB(AddressBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Address(AddressInDB):
    pass 