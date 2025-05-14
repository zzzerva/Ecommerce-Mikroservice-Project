from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.contact import Contact
from app.repository.contact_repository import ContactRepository
from app.schemas.contact import ContactCreate, ContactUpdate
from app.services.user_service import UserService

class ContactService:
    def __init__(self, db: Session):
        self.db = db
        self.contact_repository = ContactRepository(db)
        self.user_service = UserService(db)

    def get_contact(self, contact_id: int) -> Contact:
        contact = self.contact_repository.get_by_id(contact_id)
        if not contact:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contact not found"
            )
        return contact

    def get_user_contacts(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Contact]:
        self.user_service.get_user(user_id)
        return self.contact_repository.get_by_user_id(user_id, skip=skip, limit=limit)

    def create_contact(self, user_id: int, contact: ContactCreate) -> Contact:
        self.user_service.get_user(user_id) 
        return self.contact_repository.create(user_id, contact)

    def update_contact(self, contact_id: int, contact: ContactUpdate) -> Contact:
        db_contact = self.get_contact(contact_id)
        updated_contact = self.contact_repository.update(contact_id, contact)
        if not updated_contact:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contact not found"
            )
        return updated_contact

    def delete_contact(self, contact_id: int) -> bool:
        self.get_contact(contact_id)
        return self.contact_repository.delete(contact_id) 