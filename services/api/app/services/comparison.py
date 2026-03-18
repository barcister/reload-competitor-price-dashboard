from datetime import datetime, timedelta
from statistics import median

from sqlalchemy import select
from sqlalchemy.orm import Session

from services.common.db.models import NormalizedOffer, RawOffer


def build_comparison_payload(db: Session, canonical_phone_id: int, stale_hours: int = 24) -> dict:
    rows = db.execute(
        select(NormalizedOffer, RawOffer)
        .join(RawOffer, RawOffer.id == NormalizedOffer.raw_offer_id)
        .where(NormalizedOffer.canonical_phone_id == canonical_phone_id)
    ).all()
    if not rows:
        return {
            "canonical_phone_id": canonical_phone_id,
            "cheapest_offer": None,
            "median_market_price": None,
            "price_spread": None,
            "offers": [],
            "comparability_warning": "No offers",
            "stale_data_warning": True,
        }

    sorted_rows = sorted(rows, key=lambda r: float(r.NormalizedOffer.effective_total_price or r.NormalizedOffer.item_price))
    prices = [float(r.NormalizedOffer.effective_total_price or r.NormalizedOffer.item_price) for r in sorted_rows]
    cheapest = sorted_rows[0]
    cheapest_price = float(cheapest.NormalizedOffer.effective_total_price or cheapest.NormalizedOffer.item_price)
    stale_cutoff = datetime.utcnow() - timedelta(hours=stale_hours)

    offers = []
    for idx, row in enumerate(sorted_rows, start=1):
        total = float(row.NormalizedOffer.effective_total_price or row.NormalizedOffer.item_price)
        offers.append(
            {
                "rank": idx,
                "offer_id": row.NormalizedOffer.id,
                "provider_id": row.RawOffer.provider_id,
                "raw_title": row.RawOffer.raw_title,
                "normalized_title": row.NormalizedOffer.normalized_title,
                "item_price": float(row.NormalizedOffer.item_price),
                "shipping_price": float(row.NormalizedOffer.shipping_price or 0),
                "effective_total_price": total,
                "delta_vs_cheapest": round(total - cheapest_price, 2),
                "source_url": row.RawOffer.source_url,
                "updated_at": row.NormalizedOffer.updated_at.isoformat(),
                "matching_confidence": float(row.NormalizedOffer.matching_confidence or 0),
            }
        )

    comparability_warning = None
    if any(not row.NormalizedOffer.condition_grade or row.NormalizedOffer.battery_health_band == "unknown" for row in rows):
        comparability_warning = "Some offers may not be fully comparable due to missing condition/battery/warranty data."

    return {
        "canonical_phone_id": canonical_phone_id,
        "cheapest_offer": offers[0],
        "median_market_price": round(median(prices), 2),
        "price_spread": round(max(prices) - min(prices), 2),
        "offers": offers,
        "comparability_warning": comparability_warning,
        "stale_data_warning": any(r.NormalizedOffer.updated_at < stale_cutoff for r in rows),
    }
