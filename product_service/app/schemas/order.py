from pydantic import BaseModel, confloat, conint, ConfigDict
from typing import Optional, List
from datetime import datetime
from app.models.order import OrderStatus

class OrderItemBase(BaseModel):
    product_id: int
    quantity: conint(gt=0)

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemInDBBase(OrderItemBase):
    id: int
    order_id: int
    price: confloat(gt=0)
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class OrderItem(OrderItemInDBBase):
    pass

class OrderBase(BaseModel):
    user_id: int
    shipping_address: str

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    shipping_address: Optional[str] = None

class OrderInDBBase(OrderBase):
    id: int
    status: OrderStatus
    total_amount: confloat(gt=0)
    created_at: datetime
    updated_at: Optional[datetime] = None
    items: List[OrderItem] = []

    model_config = ConfigDict(from_attributes=True)

class Order(OrderInDBBase):
    pass 