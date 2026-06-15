from datetime import datetime

from pydantic import BaseModel, Field


class ScanCreate(BaseModel):
    barcode: str = Field(min_length=3, max_length=32)
    source: str | None = None


class ScanRead(BaseModel):
    id: int
    barcode: str
    source: str | None
    deposit_cents: int
    scanned_at: datetime

    model_config = {"from_attributes": True}