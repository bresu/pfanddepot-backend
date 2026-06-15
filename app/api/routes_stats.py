from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.scan import Scan
from app.schemas.stats import StatsRead

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("", response_model=StatsRead)
def get_stats(db: Session = Depends(get_db)):
    """Returns total number of items, total cents and total euros."""
    total_items = db.query(func.count(Scan.id)).scalar() or 0
    total_cents = db.query(func.sum(Scan.deposit_cents)).scalar() or 0

    return {
        "total_items": total_items,
        "total_cents": total_cents,
        "total_euros": total_cents / 100,
    }