from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, HttpUrl


class OfferIn(BaseModel):
    retailer: str
    source_url: HttpUrl
    raw_title: str
    price: Decimal
    currency: str
    shipping_cost: Optional[Decimal] = None
    availability: Optional[str] = None
    condition_grade: Optional[str] = None
    battery_health_percent: Optional[int] = None
    warranty_months: Optional[int] = None
    extraction_confidence: float = 0.7
    source_type: str = "structured_data"
    payload: dict = {}


class OfferOut(BaseModel):
    id: int
    normalized_title: str
    current_price: Decimal
    effective_total_price: Optional[Decimal]
    currency: str
    matching_confidence: Optional[Decimal]
    updated_at: datetime


class CompareResponse(BaseModel):
    canonical_phone_id: int
    cheapest_offer_id: Optional[int]
    cheapest_price: Optional[Decimal]
    median_market_price: Optional[Decimal]
    price_spread: Optional[Decimal]
    stale_data_warning: bool
    notes: list[str]
    offers: list[dict]
