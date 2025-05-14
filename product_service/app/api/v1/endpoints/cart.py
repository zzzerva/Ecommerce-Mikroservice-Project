from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.cart import Cart, CartCreate, CartItem, CartItemCreate, CartItemUpdate
from app.services.cart import cart_service
from app.api.deps import get_current_active_user

router = APIRouter()

@router.get("/", response_model=Cart)
def read_cart(
    *,
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_current_active_user),
) -> Any:
    """
    Get current user's cart.
    """
    cart = cart_service.get_by_user_id(db, user_id=current_user.id)
    if not cart:
        cart = cart_service.create(db, user_id=current_user.id)
    return cart

@router.post("/items/", response_model=CartItem)
def add_cart_item(
    *,
    db: Session = Depends(get_db),
    item_in: CartItemCreate,
    current_user: Any = Depends(get_current_active_user),
) -> Any:
    """
    Add item to cart.
    """
    cart = cart_service.get_by_user_id(db, user_id=current_user.id)
    if not cart:
        cart = cart_service.create(db, user_id=current_user.id)
    
    try:
        cart_item = cart_service.add_item(
            db,
            cart_id=cart.id,
            product_id=item_in.product_id,
            quantity=item_in.quantity
        )
        return cart_item
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.put("/items/{item_id}", response_model=CartItem)
def update_cart_item(
    *,
    db: Session = Depends(get_db),
    item_id: int,
    item_in: CartItemUpdate,
    current_user: Any = Depends(get_current_active_user),
) -> Any:
    """
    Update cart item quantity.
    """
    cart = cart_service.get_by_user_id(db, user_id=current_user.id)
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart not found"
        )
    
    try:
        cart_item = cart_service.update_item(
            db,
            cart_id=cart.id,
            item_id=item_id,
            quantity=item_in.quantity
        )
        return cart_item
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/items/{item_id}", response_model=CartItem)
def remove_cart_item(
    *,
    db: Session = Depends(get_db),
    item_id: int,
    current_user: Any = Depends(get_current_active_user),
) -> Any:
    """
    Remove item from cart.
    """
    cart = cart_service.get_by_user_id(db, user_id=current_user.id)
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart not found"
        )
    
    try:
        cart_item = cart_service.remove_item(db, cart_id=cart.id, item_id=item_id)
        return cart_item
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/clear", response_model=None)
def clear_cart(
    db: Session = Depends(get_db),
    current_user: Any = Depends(get_current_active_user),
):
    cart = cart_service.get_by_user_id(db, user_id=current_user.id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    cart_service.clear_cart(db, cart_id=cart.id)
    return Response(status_code=200) 