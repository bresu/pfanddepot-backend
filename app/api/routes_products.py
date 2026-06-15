from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate


router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=list[ProductRead])
def get_products(db: Session = Depends(get_db)):
    products = db.scalars(
        select(Product).order_by(Product.created_at.desc())
    ).all()

    return products


@router.get("/{barcode}", response_model=ProductRead)
def get_product(barcode: str, db: Session = Depends(get_db)):
    product = db.scalar(
        select(Product).where(Product.barcode == barcode)
    )

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    return product


@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(product_in: ProductCreate, db: Session = Depends(get_db)):
    product = Product(**product_in.model_dump())

    db.add(product)

    try:
        db.commit()
        db.refresh(product)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Product with this barcode already exists",
        )

    return product


@router.put("/{barcode}", response_model=ProductRead)
def update_product(
    barcode: str,
    product_in: ProductUpdate,
    db: Session = Depends(get_db),
):
    product = db.scalar(
        select(Product).where(Product.barcode == barcode)
    )

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    update_data = product_in.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)

    return product


@router.delete("/{barcode}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(barcode: str, db: Session = Depends(get_db)):
    product = db.scalar(
        select(Product).where(Product.barcode == barcode)
    )

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    db.delete(product)
    db.commit()

    return None