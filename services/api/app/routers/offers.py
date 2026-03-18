from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from services.api.app.services.comparison import build_comparison_payload
from services.common.db.models import NormalizedOffer, PriceHistory, RawOffer
from services.common.db.session import get_db

router = APIRouter(prefix="/offers", tags=["offers"])


@router.get("")
def list_offers(
    provider: int | None = Query(default=None),
    condition_grade: str | None = Query(default=None),
    battery_health_band: str | None = Query(default=None),
    availability: str | None = Query(default=None),
    updated_after: datetime | None = Query(default=None),
    db: Session = Depends(get_db),
):
    stmt = select(NormalizedOffer, RawOffer).join(RawOffer, RawOffer.id == NormalizedOffer.raw_offer_id)
    if provider:
        stmt = stmt.where(RawOffer.provider_id == provider)
    if condition_grade:
        stmt = stmt.where(NormalizedOffer.condition_grade == condition_grade)
    if battery_health_band:
        stmt = stmt.where(NormalizedOffer.battery_health_band == battery_health_band)
    if availability:
        stmt = stmt.where(NormalizedOffer.availability == availability)
    if updated_after:
        stmt = stmt.where(NormalizedOffer.updated_at >= updated_after)
    return [
        {
            "offer_id": row.NormalizedOffer.id,
            "provider_id": row.RawOffer.provider_id,
            "raw_title": row.RawOffer.raw_title,
            "normalized_title": row.NormalizedOffer.normalized_title,
            "item_price": row.NormalizedOffer.item_price,
            "shipping_price": row.NormalizedOffer.shipping_price,
            "effective_total_price": row.NormalizedOffer.effective_total_price,
            "effective_total_uncertain": row.NormalizedOffer.effective_total_uncertain,
            "currency": row.NormalizedOffer.currency,
            "matching_confidence": row.NormalizedOffer.matching_confidence,
            "source_url": row.RawOffer.source_url,
        }
        for row in db.execute(stmt).all()
    ]


@router.get("/{canonical_phone_id}/compare")
def compare(canonical_phone_id: int, db: Session = Depends(get_db)):
    return build_comparison_payload(db, canonical_phone_id)


@router.get("/{canonical_phone_id}/history")
def history(canonical_phone_id: int, db: Session = Depends(get_db)):
    stmt = (
        select(PriceHistory)
        .join(NormalizedOffer, PriceHistory.normalized_offer_id == NormalizedOffer.id)
        .where(NormalizedOffer.canonical_phone_id == canonical_phone_id)
        .order_by(PriceHistory.captured_at.asc())
    )
    return db.execute(stmt).scalars().all()
