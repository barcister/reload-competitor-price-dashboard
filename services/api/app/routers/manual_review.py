from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from services.common.db.models import ManualMatchReview, NormalizedOffer
from services.common.db.session import get_db

router = APIRouter(prefix="/manual-review", tags=["manual-review"])


class ResolvePayload(BaseModel):
    canonical_phone_id: int


@router.get("")
def list_reviews(db: Session = Depends(get_db)):
    return db.execute(select(ManualMatchReview).where(ManualMatchReview.status == "pending")).scalars().all()


@router.post("/{review_id}/resolve")
def resolve(review_id: int, payload: ResolvePayload, db: Session = Depends(get_db)):
    review = db.get(ManualMatchReview, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    offer = db.get(NormalizedOffer, review.normalized_offer_id)
    offer.canonical_phone_id = payload.canonical_phone_id
    offer.match_reason = "manual review"
    offer.matching_confidence = 1
    review.status = "resolved"
    review.resolved_at = datetime.utcnow()
    db.add_all([offer, review])
    db.commit()
    return {"status": "resolved"}
