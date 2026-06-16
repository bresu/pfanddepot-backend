from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.enums import ProductType, ReturnLocation


class ProductBase(BaseModel):
    barcode: str = Field(..., min_length=1, max_length=64)
    name: str = Field(..., min_length=1)
    brand: str | None = None

    product_type: ProductType = ProductType.bottle

    is_returnable: bool = True
    is_verified: bool = True

    return_locations: list[ReturnLocation] | None = None
    thumbnail_url: str | None = None

    deposit_cents: int = Field(default=25, ge=0)


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    brand: str | None = None

    product_type: ProductType | None = None

    is_returnable: bool | None = None
    is_verified: bool | None = None

    return_locations: list[ReturnLocation] | None = None
    thumbnail_url: str | None = None

    deposit_cents: int | None = Field(default=None, ge=0)


class ProductRead(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)