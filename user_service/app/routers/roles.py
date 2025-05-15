from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.dependencies import require_role
from app.schemas import RoleCreate, RoleUpdate, PermissionAdd

router = APIRouter()

@router.post("/roles", status_code=status.HTTP_201_CREATED)
async def create_role(
    role: RoleCreate,
    db: Session = Depends(get_db),
    _: str = Depends(require_role(["Admin"]))
):
    db_role = models.Role(**role.model_dump())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

@router.put("/roles/{role_id}")
async def update_role(
    role_id: int,
    role_update: RoleUpdate,
    db: Session = Depends(get_db),
    _: str = Depends(require_role(["Admin"]))
):
    db_role = db.query(models.Role).filter(models.Role.id == role_id).first()
    if not db_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
    
    db_role.permissions = role_update.permissions
    db.commit()
    db.refresh(db_role)
    return db_role

@router.post("/roles/{role_id}/permissions")
async def add_permission(
    role_id: int,
    permission: PermissionAdd,
    db: Session = Depends(get_db),
    _: str = Depends(require_role(["Admin"]))
):
    db_role = db.query(models.Role).filter(models.Role.id == role_id).first()
    if not db_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )
    
    if permission.permission not in db_role.permissions:
        db_role.permissions.append(permission.permission)
        db.commit()
        db.refresh(db_role)
    
    return db_role