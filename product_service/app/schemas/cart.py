from pydantic import BaseModel, conint, confloat, ConfigDict
from typing import Optional, List
from datetime import datetime

class CartItemBase(BaseModel):
    product_id: int
    quantity: conint(gt=0)

class CartItemCreate(CartItemBase):
    pass

class CartItemUpdate(BaseModel):
    quantity: Optional[conint(gt=0)] = None

class CartItemInDBBase(CartItemBase):
    id: int
    cart_id: int
    price: confloat(gt=0)
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class CartItem(CartItemInDBBase):
    pass

class CartBase(BaseModel):
    user_id: int

class CartCreate(CartBase):
    pass

class CartInDBBase(CartBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    items: List[CartItem] = []

    model_config = ConfigDict(from_attributes=True)

class Cart(CartInDBBase):
    pass 