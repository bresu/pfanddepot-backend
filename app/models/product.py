from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String, Boolean
from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


"""
type Product = {
  barcode: string
  name: string
  brand?: string
  is_returnable: boolean
  return_locations?: string[]
  thumbnail_url?: string
  deposit_cents: number
  created_at: string
  updated_at: string
}"""

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    barcode: Mapped[str] = mapped_column(String, index=True, unique=True)
    name: Mapped[str] = mapped_column(String, index=True)
    brand: Mapped[str | None] = mapped_column(String, nullable=True)
    is_returnable: Mapped[bool] = mapped_column(Boolean, default=True)
    return_locations: Mapped[list[str] | None] = mapped_column(JSON,nullable=True,)
    thumbnail_url: Mapped[str | None] = mapped_column(String, nullable=True)
    deposit_cents: Mapped[int] = mapped_column(Integer, default=25)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )