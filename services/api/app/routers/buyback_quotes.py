from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from services.common.db.models import BuybackQuote
from services.common.db.session import get_db

router = APIRouter(prefix="/buyback-quotes", tags=["buyback"])


@router.get("")
def list_buyback_quotes(provider: int | None = Query(default=None), db: Session = Depends(get_db)):
    stmt = select(BuybackQuote)
    if provider:
        stmt = stmt.where(BuybackQuote.provider_id == provider)
    return db.execute(stmt).scalars().all()
