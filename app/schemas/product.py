from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    barcode: str = Field(..., min_length=1, max_length=64)
    name: str = Field(..., min_length=1)
    brand: str | None = None
    is_returnable: bool = True
    return_locations: list[str] | None = None
    thumbnail_url: str | None = None
    deposit_cents: int = Field(default=25, ge=0)


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    brand: str | None = None
    is_returnable: bool | None = None
    return_locations: list[str] | None = None
    thumbnail_url: str | None = None
    deposit_cents: int | None = Field(default=None, ge=0)


class ProductRead(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)