from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.scan import Scan
from app.schemas.scan import ScanCreate, ScanRead

router = APIRouter(prefix="/scans", tags=["scans"])


@router.post("", response_model=ScanRead)
def create_scan(scan_in: ScanCreate, db: Session = Depends(get_db)):
    """Create a scan object, default source is None and default deposit = 25 cents."""
    scan = Scan(
        barcode=scan_in.barcode,
        source=scan_in.source,
        deposit_cents=25,
    )

    db.add(scan)
    db.commit()
    db.refresh(scan)

    return scan


@router.get("", response_model=list[ScanRead])
def list_scans(db: Session = Depends(get_db)):
    """List the most recent scans. Limit 50."""
    return db.query(Scan).order_by(Scan.scanned_at.desc()).limit(50).all()


@router.delete("/{scan_id}", status_code=204)
def delete_scan(scan_id: int, db: Session = Depends(get_db)):
    """Delete a scan by ID. Returns 404 if ID doesnt exist."""
    scan = db.get(Scan, scan_id)

    if scan is None:
        raise HTTPException(404, "Scan not found")

    db.delete(scan)
    db.commit()