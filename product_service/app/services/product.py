from typing import Any, Dict, List, Optional, Union
from sqlalchemy.orm import Session
from app.models.product import Product, Category
from app.schemas.product import ProductCreate, ProductUpdate, CategoryCreate, CategoryUpdate

class ProductService:
    def get(self, db: Session, id: Any) -> Optional[Product]:
        return db.query(Product).filter(Product.id == id).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Product]:
        return db.query(Product).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: ProductCreate) -> Product:
        db_obj = Product(
            name=obj_in.name,
            description=obj_in.description,
            price=obj_in.price,
            stock=obj_in.stock,
            category_id=obj_in.category_id,
            is_active=obj_in.is_active,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: Product,
        obj_in: Union[ProductUpdate, Dict[str, Any]]
    ) -> Product:
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

    def remove(self, db: Session, *, id: int) -> Product:
        obj = db.query(Product).get(id)
        db.delete(obj)
        db.commit()
        return obj

class CategoryService:
    def get(self, db: Session, id: Any) -> Optional[Category]:
        return db.query(Category).filter(Category.id == id).first()

    def get_by_name(self, db: Session, name: str) -> Optional[Category]:
        return db.query(Category).filter(Category.name == name).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Category]:
        return db.query(Category).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CategoryCreate) -> Category:
        db_obj = Category(
            name=obj_in.name,
            description=obj_in.description,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: Category,
        obj_in: Union[CategoryUpdate, Dict[str, Any]]
    ) -> Category:
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

    def remove(self, db: Session, *, id: int) -> Category:
        obj = db.query(Category).get(id)
        db.delete(obj)
        db.commit()
        return obj

product_service = ProductService()
category_service = CategoryService() 