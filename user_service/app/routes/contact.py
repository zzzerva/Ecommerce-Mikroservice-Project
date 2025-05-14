from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.contact_service import ContactService
from app.schemas.contact import Contact, ContactCreate, ContactUpdate
from app.routes.user import get_current_user
from app.schemas.user import User

router = APIRouter(prefix="/contact", tags=["contact"])

@router.get("/", response_model=List[Contact])
def list_contacts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    contact_service = ContactService(db)
    return contact_service.get_user_contacts(current_user.id, skip=skip, limit=limit)

@router.post("/", response_model=Contact)
def create_contact(
    contact: ContactCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    contact_service = ContactService(db)
    return contact_service.create_contact(current_user.id, contact)

@router.get("/{contact_id}", response_model=Contact)
def read_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    contact_service = ContactService(db)
    contact = contact_service.get_contact(contact_id)
    if contact.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return contact

@router.put("/{contact_id}", response_model=Contact)
def update_contact(
    contact_id: int,
    contact: ContactUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    contact_service = ContactService(db)
    db_contact = contact_service.get_contact(contact_id)
    if db_contact.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return contact_service.update_contact(contact_id, contact)

@router.delete("/{contact_id}")
def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    contact_service = ContactService(db)
    db_contact = contact_service.get_contact(contact_id)
    if db_contact.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return contact_service.delete_contact(contact_id) 