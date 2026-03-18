from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from services.common.db.models import CanonicalPhone
from services.common.db.session import get_db

router = APIRouter(prefix="/phones", tags=["phones"])


@router.get("")
def list_phones(
    brand: str | None = Query(default=None),
    model_family: str | None = Query(default=None),
    storage: int | None = Query(default=None),
    db: Session = Depends(get_db),
):
    stmt = select(CanonicalPhone)
    if brand:
        stmt = stmt.where(CanonicalPhone.brand.ilike(f"%{brand}%"))
    if model_family:
        stmt = stmt.where(CanonicalPhone.model_family.ilike(f"%{model_family}%"))
    if storage:
        stmt = stmt.where(CanonicalPhone.storage_gb == storage)
    return db.execute(stmt).scalars().all()


@router.get("/{canonical_phone_id}")
def phone_detail(canonical_phone_id: int, db: Session = Depends(get_db)):
    phone = db.get(CanonicalPhone, canonical_phone_id)
    if not phone:
        raise HTTPException(status_code=404, detail="Phone not found")
    return phone
