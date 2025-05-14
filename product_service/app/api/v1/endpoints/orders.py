from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.order import Order, OrderCreate, OrderUpdate
from app.services.order import order_service
from app.api.deps import get_current_active_user, get_current_active_admin

router = APIRouter()

@router.post("/", response_model=Order)
def create_order(
    *,
    db: Session = Depends(get_db),
    order_in: OrderCreate,
    current_user: Any = Depends(get_current_active_user),
) -> Any:
    """
    Create new order.
    """
    try:
        order = order_service.create(db, obj_in=order_in)
        return order
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/from-cart/", response_model=Order)
def create_order_from_cart(
    *,
    db: Session = Depends(get_db),
    shipping_address: str,
    current_user: Any = Depends(get_current_active_user),
) -> Any:
    """
    Create new order from user's cart.
    """
    try:
        order = order_service.create_from_cart(
            db,
            user_id=current_user.id,
            shipping_address=shipping_address
        )
        return order
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=List[Order])
def read_orders(
    *,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: Any = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve orders for current user.
    """
    orders = order_service.get_by_user(db, user_id=current_user.id, skip=skip, limit=limit)
    return orders

@router.get("/{order_id}", response_model=Order)
def read_order(
    *,
    db: Session = Depends(get_db),
    order_id: int,
    current_user: Any = Depends(get_current_active_user),
) -> Any:
    """
    Get order by ID.
    """
    order = order_service.get(db, id=order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    if order.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return order

@router.put("/{order_id}", response_model=Order)
def update_order(
    *,
    db: Session = Depends(get_db),
    order_id: int,
    order_in: OrderUpdate,
    current_user: Any = Depends(get_current_active_admin),
) -> Any:
    """
    Update an order.
    """
    order = order_service.get(db, id=order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    order = order_service.update(db, db_obj=order, obj_in=order_in)
    return order

@router.post("/{order_id}/cancel", response_model=Order)
def cancel_order(
    *,
    db: Session = Depends(get_db),
    order_id: int,
    current_user: Any = Depends(get_current_active_user),
) -> Any:
    """
    Cancel an order.
    """
    order = order_service.get(db, id=order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    if order.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    try:
        order = order_service.cancel(db, order_id=order_id)
        return order
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) 