from typing import Any, Dict, List, Optional, Union
from sqlalchemy.orm import Session
from app.models.cart import Cart, CartItem
from app.models.product import Product
from app.schemas.cart import CartCreate, CartItemCreate, CartItemUpdate

class CartService:
    def get(self, db: Session, id: Any) -> Optional[Cart]:
        return db.query(Cart).filter(Cart.id == id).first()

    def get_by_user(self, db: Session, user_id: int) -> Optional[Cart]:
        return db.query(Cart).filter(Cart.user_id == user_id).first()

    def get_by_user_id(self, db: Session, user_id: int) -> Optional[Cart]:
        # Alias for compatibility
        return self.get_by_user(db, user_id)

    def create(self, db: Session, *, obj_in: Optional[CartCreate] = None, user_id: Optional[int] = None) -> Cart:
        if obj_in is None and user_id is not None:
            obj_in = CartCreate(user_id=user_id)
        elif obj_in is None:
            raise ValueError("Either obj_in or user_id must be provided")
        db_obj = Cart(user_id=obj_in.user_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_or_create(self, db: Session, *, user_id: int) -> Cart:
        cart = self.get_by_user(db, user_id=user_id)
        if not cart:
            cart = self.create(db, user_id=user_id)
        return cart

    def add_item(
        self,
        db: Session,
        *,
        cart_id: int,
        item_in: Optional[CartItemCreate] = None,
        product_id: Optional[int] = None,
        quantity: Optional[int] = None
    ) -> CartItem:
        if item_in is None and product_id is not None and quantity is not None:
            item_in = CartItemCreate(product_id=product_id, quantity=quantity)
        elif item_in is None:
            raise ValueError("Either item_in or (product_id and quantity) must be provided")
        product = db.query(Product).filter(Product.id == item_in.product_id).first()
        if not product:
            raise ValueError("Product not found")
        if product.stock < item_in.quantity:
            raise ValueError("Not enough stock")

        # Aynı üründen varsa miktarı artır
        cart_item = db.query(CartItem).filter(
            CartItem.cart_id == cart_id,
            CartItem.product_id == item_in.product_id
        ).first()
        if cart_item:
            cart_item.quantity += item_in.quantity
            db.add(cart_item)
            db.commit()
            db.refresh(cart_item)
            return cart_item
        else:
            cart_item = CartItem(
                cart_id=cart_id,
                product_id=item_in.product_id,
                quantity=item_in.quantity,
                price=product.price
            )
            db.add(cart_item)
            db.commit()
            db.refresh(cart_item)
            return cart_item

    def update_item(
        self,
        db: Session,
        *,
        cart_id: int,
        item_id: int,
        item_in: CartItemUpdate
    ) -> CartItem:
        cart_item = (
            db.query(CartItem)
            .filter(CartItem.cart_id == cart_id, CartItem.id == item_id)
            .first()
        )
        if not cart_item:
            raise ValueError("Cart item not found")

        if item_in.quantity:
            product = db.query(Product).filter(Product.id == cart_item.product_id).first()
            if product.stock < item_in.quantity:
                raise ValueError("Not enough stock")
            cart_item.quantity = item_in.quantity

        db.add(cart_item)
        db.commit()
        db.refresh(cart_item)
        return cart_item

    def remove_item(self, db: Session, *, cart_id: int, item_id: int) -> CartItem:
        cart_item = (
            db.query(CartItem)
            .filter(CartItem.cart_id == cart_id, CartItem.id == item_id)
            .first()
        )
        if not cart_item:
            raise ValueError("Cart item not found")
        db.delete(cart_item)
        db.commit()
        return cart_item

    def clear_cart(self, db: Session, *, cart_id: int) -> None:
        db.query(CartItem).filter(CartItem.cart_id == cart_id).delete()
        db.commit()

cart_service = CartService() 