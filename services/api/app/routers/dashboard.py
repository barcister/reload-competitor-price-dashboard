from sqlalchemy import func, select
from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends

from services.common.db.models import NormalizedOffer, Provider
from services.common.db.session import get_db

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary")
def summary(db: Session = Depends(get_db)):
    providers = db.scalar(select(func.count()).select_from(Provider)) or 0
    offers = db.scalar(select(func.count()).select_from(NormalizedOffer)) or 0
    avg_price = db.scalar(select(func.avg(NormalizedOffer.effective_total_price)))
    return {
        "provider_count": providers,
        "offer_count": offers,
        "average_effective_price": float(avg_price) if avg_price else None,
    }
