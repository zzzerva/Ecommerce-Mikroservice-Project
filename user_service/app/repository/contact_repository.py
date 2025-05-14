from sqlalchemy.orm import Session
from app.models.contact import Contact
from app.schemas.contact import ContactCreate, ContactUpdate
from typing import List, Optional

class ContactRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, contact_id: int) -> Optional[Contact]:
        return self.db.query(Contact).filter(Contact.id == contact_id).first()

    def get_by_user_id(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Contact]:
        return self.db.query(Contact).filter(Contact.user_id == user_id).offset(skip).limit(limit).all()

    def create(self, user_id: int, contact: ContactCreate) -> Contact:
        db_contact = Contact(**contact.model_dump(), user_id=user_id)
        self.db.add(db_contact)
        self.db.commit()
        self.db.refresh(db_contact)
        return db_contact

    def update(self, contact_id: int, contact: ContactUpdate) -> Optional[Contact]:
        db_contact = self.get_by_id(contact_id)
        if not db_contact:
            return None

        update_data = contact.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_contact, field, value)

        self.db.commit()
        self.db.refresh(db_contact)
        return db_contact

    def delete(self, contact_id: int) -> bool:
        db_contact = self.get_by_id(contact_id)
        if not db_contact:
            return False
        self.db.delete(db_contact)
        self.db.commit()
        return True 