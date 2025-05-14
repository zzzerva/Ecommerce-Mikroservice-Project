from pydantic import BaseModel, confloat, conint, ConfigDict
from typing import Optional, List
from datetime import datetime

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    name: Optional[str] = None

class CategoryInDBBase(CategoryBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class Category(CategoryInDBBase):
    pass

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: confloat(gt=0)
    stock: conint(ge=0)
    category_id: int
    is_active: Optional[bool] = True

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[confloat(gt=0)] = None
    stock: Optional[conint(ge=0)] = None
    category_id: Optional[int] = None
    is_active: Optional[bool] = None

class ProductInDBBase(ProductBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class Product(ProductInDBBase):
    category: Category 