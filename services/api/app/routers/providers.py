from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from services.common.db.models import ConnectorHealthSnapshot, Provider
from services.common.db.session import get_db

router = APIRouter(prefix="/providers", tags=["providers"])


@router.get("")
def list_providers(db: Session = Depends(get_db)):
    return db.execute(select(Provider)).scalars().all()


@router.get("/{provider_id}")
def get_provider(provider_id: int, db: Session = Depends(get_db)):
    provider = db.get(Provider, provider_id)
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    return provider


@router.get("/{provider_id}/status")
def provider_status(provider_id: int, db: Session = Depends(get_db)):
    status = (
        db.execute(
            select(ConnectorHealthSnapshot)
            .where(ConnectorHealthSnapshot.provider_id == provider_id)
            .order_by(ConnectorHealthSnapshot.checked_at.desc())
        )
        .scalars()
        .first()
    )
    if not status:
        raise HTTPException(status_code=404, detail="No status snapshot")
    return status
