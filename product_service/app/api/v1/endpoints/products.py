from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.product import Product, ProductCreate, ProductUpdate, Category, CategoryCreate, CategoryUpdate
from app.services.product import product_service, category_service
from app.api.deps import get_current_active_user, get_current_active_admin

router = APIRouter()

# Category endpoints
@router.post("/categories/", response_model=Category)
def create_category(
    *,
    db: Session = Depends(get_db),
    category_in: CategoryCreate,
    current_user: Any = Depends(get_current_active_admin),
) -> Any:
    """
    Create new category.
    """
    category = category_service.get_by_name(db, name=category_in.name)
    if category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category with this name already exists",
        )
    category = category_service.create(db, obj_in=category_in)
    return category

@router.get("/categories/", response_model=List[Category])
def read_categories(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve categories.
    """
    categories = category_service.get_multi(db, skip=skip, limit=limit)
    return categories

@router.get("/categories/{category_id}", response_model=Category)
def read_category(
    *,
    db: Session = Depends(get_db),
    category_id: int,
) -> Any:
    """
    Get category by ID.
    """
    category = category_service.get(db, id=category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    return category

@router.put("/categories/{category_id}", response_model=Category)
def update_category(
    *,
    db: Session = Depends(get_db),
    category_id: int,
    category_in: CategoryUpdate,
    current_user: Any = Depends(get_current_active_admin),
) -> Any:
    """
    Update a category.
    """
    category = category_service.get(db, id=category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    category = category_service.update(db, db_obj=category, obj_in=category_in)
    return category

@router.delete("/categories/{category_id}", response_model=Category)
def delete_category(
    *,
    db: Session = Depends(get_db),
    category_id: int,
    current_user: Any = Depends(get_current_active_admin),
) -> Any:
    """
    Delete a category.
    """
    category = category_service.get(db, id=category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    category = category_service.remove(db, id=category_id)
    return category

# Product endpoints
@router.post("/", response_model=Product)
def create_product(
    *,
    db: Session = Depends(get_db),
    product_in: ProductCreate,
    current_user: Any = Depends(get_current_active_admin),
) -> Any:
    """
    Create new product.
    """
    category = category_service.get(db, id=product_in.category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    product = product_service.create(db, obj_in=product_in)
    return product

@router.get("/", response_model=List[Product])
def read_products(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve products.
    """
    products = product_service.get_multi(db, skip=skip, limit=limit)
    return products

@router.get("/{product_id}", response_model=Product)
def read_product(
    *,
    db: Session = Depends(get_db),
    product_id: int,
) -> Any:
    """
    Get product by ID.
    """
    product = product_service.get(db, id=product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return product

@router.put("/{product_id}", response_model=Product)
def update_product(
    *,
    db: Session = Depends(get_db),
    product_id: int,
    product_in: ProductUpdate,
    current_user: Any = Depends(get_current_active_admin),
) -> Any:
    """
    Update a product.
    """
    product = product_service.get(db, id=product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    if product_in.category_id:
        category = category_service.get(db, id=product_in.category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found",
            )
    product = product_service.update(db, db_obj=product, obj_in=product_in)
    return product

@router.delete("/{product_id}", response_model=Product)
def delete_product(
    *,
    db: Session = Depends(get_db),
    product_id: int,
    current_user: Any = Depends(get_current_active_admin),
) -> Any:
    """
    Delete a product.
    """
    product = product_service.get(db, id=product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    product = product_service.remove(db, id=product_id)
    return product 