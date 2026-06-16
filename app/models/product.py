from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    barcode: Mapped[str] = mapped_column(
        String,
        unique=True,
        index=True,
        nullable=False,
    )

    name: Mapped[str] = mapped_column(String, index=True, nullable=False)
    brand: Mapped[str | None] = mapped_column(String, nullable=True)

    product_type: Mapped[str] = mapped_column(
        String,
        default="bottle",
        nullable=False,
    )

    is_returnable: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    return_locations: Mapped[list[str] | None] = mapped_column(
        JSON,
        nullable=True,
    )

    thumbnail_url: Mapped[str | None] = mapped_column(String, nullable=True)

    deposit_cents: Mapped[int] = mapped_column(
        Integer,
        default=25,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )