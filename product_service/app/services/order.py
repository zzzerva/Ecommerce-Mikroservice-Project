from typing import Any, Dict, List, Optional, Union
from sqlalchemy.orm import Session
from app.models.order import Order, OrderItem, OrderStatus
from app.models.product import Product
from app.schemas.order import OrderCreate, OrderUpdate
from app.services.cart import cart_service

class OrderService:
    def get(self, db: Session, id: Any) -> Optional[Order]:
        return db.query(Order).filter(Order.id == id).first()

    def get_by_user(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Order]:
        return (
            db.query(Order)
            .filter(Order.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, db: Session, *, obj_in: OrderCreate) -> Order:
        # Calculate total amount
        total_amount = 0
        order_items = []

        for item in obj_in.items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            if not product:
                raise ValueError(f"Product {item.product_id} not found")
            if product.stock < item.quantity:
                raise ValueError(f"Not enough stock for product {product.name}")
            
            total_amount += product.price * item.quantity
            order_items.append(
                OrderItem(
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price=product.price
                )
            )
            # Update product stock
            product.stock -= item.quantity
            db.add(product)
            db.commit()
            db.refresh(product)

        # Create order
        db_obj = Order(
            user_id=obj_in.user_id,
            status=OrderStatus.PENDING,
            total_amount=total_amount,
            shipping_address=obj_in.shipping_address,
            items=order_items
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_from_cart(
        self, db: Session, *, user_id: int, shipping_address: str
    ) -> Order:
        # Get user's cart
        cart = cart_service.get_by_user(db, user_id=user_id)
        if not cart or not cart.items:
            raise ValueError("Cart is empty")

        # Calculate total amount and prepare order items
        total_amount = 0
        order_items = []

        for cart_item in cart.items:
            product = db.query(Product).filter(Product.id == cart_item.product_id).first()
            if not product:
                raise ValueError(f"Product {cart_item.product_id} not found")
            if product.stock < cart_item.quantity:
                raise ValueError(f"Not enough stock for product {product.name}")
            
            total_amount += cart_item.price * cart_item.quantity
            order_items.append(
                OrderItem(
                    product_id=cart_item.product_id,
                    quantity=cart_item.quantity,
                    price=cart_item.price
                )
            )
            # Update product stock
            product.stock -= cart_item.quantity
            db.add(product)
            db.commit()
            db.refresh(product)

        # Create order
        db_obj = Order(
            user_id=user_id,
            status=OrderStatus.PENDING,
            total_amount=total_amount,
            shipping_address=shipping_address,
            items=order_items
        )
        db.add(db_obj)
        
        # Clear cart
        cart_service.clear_cart(db, cart_id=cart.id)
        
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: Order,
        obj_in: Union[OrderUpdate, Dict[str, Any]]
    ) -> Order:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        for field in update_data:
            setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def cancel(self, db: Session, *, order_id: int) -> Order:
        order = self.get(db, id=order_id)
        if not order:
            raise ValueError("Order not found")
        if order.status != OrderStatus.PENDING:
            raise ValueError("Can only cancel pending orders")

        # Restore product stock
        for item in order.items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            if product:
                product.stock += item.quantity
                db.add(product)
                db.commit()
                db.refresh(product)

        order.status = OrderStatus.CANCELLED
        db.add(order)
        db.commit()
        db.refresh(order)
        return order

order_service = OrderService() 