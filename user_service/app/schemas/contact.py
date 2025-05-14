from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.models.contact import ContactType

class ContactBase(BaseModel):
    type: ContactType
    phone: str
    email: EmailStr
    is_default: bool = False

class ContactCreate(ContactBase):
    pass

class ContactUpdate(BaseModel):
    type: Optional[ContactType] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    is_default: Optional[bool] = None

class ContactInDB(ContactBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Contact(ContactInDB):
    pass 