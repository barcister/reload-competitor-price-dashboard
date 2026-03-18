from decimal import Decimal

from services.common.db.models import CanonicalPhone, NormalizedOffer, PriceHistory, Provider, RawOffer
from services.common.db.session import SessionLocal
from services.common.utils.normalization import battery_health_band, effective_total_price


def seed() -> None:
    db = SessionLocal()
    try:
        if db.query(Provider).count() > 0:
            return

        revendo = Provider(
            storefront_name="Revendo",
            underlying_provider_name="Revendo",
            provider_type="LISTING_SOURCE",
            automation_level="static",
            reliability_score=Decimal("0.92"),
            reliability_status="healthy",
            support_level="FULL_SUPPORT",
        )
        refurbed = Provider(
            storefront_name="refurbed.ch",
            underlying_provider_name="Refurbed Marketplace",
            provider_type="MARKETPLACE_SOURCE",
            automation_level="dynamic",
            reliability_score=Decimal("0.88"),
            reliability_status="healthy",
            supports_marketplace_seller_identity=True,
            support_level="FULL_SUPPORT",
        )
        db.add_all([revendo, refurbed])
        db.flush()

        phone = CanonicalPhone(
            brand="Apple",
            model_family="iPhone",
            model_name="iPhone 14 Pro",
            generation="14",
            storage_gb=128,
            color="Space Gray",
            condition_grade="Excellent",
            battery_health_percent=91,
            battery_health_band="90_to_94",
            warranty_months=12,
            release_year=2022,
        )
        db.add(phone)
        db.flush()

        raw = RawOffer(
            provider_id=revendo.id,
            source_url="https://www.revendo.example/ch/iphone-14",
            source_identifier="REV-001",
            raw_title="Apple iPhone 14 Pro 128GB Space Gray",
            extraction_mode="structured_data",
            extraction_confidence=Decimal("0.90"),
            payload={"seed": True},
        )
        db.add(raw)
        db.flush()

        effective, uncertain = effective_total_price(Decimal("699.00"), Decimal("0.00"))
        normalized = NormalizedOffer(
            raw_offer_id=raw.id,
            canonical_phone_id=phone.id,
            normalized_title="iPhone 14 Pro 128GB Space Gray",
            item_price=Decimal("699.00"),
            shipping_price=Decimal("0.00"),
            effective_total_price=effective,
            effective_total_uncertain=uncertain,
            currency="CHF",
            availability="in_stock",
            condition_grade="Excellent",
            battery_health_percent=91,
            battery_health_band=battery_health_band(91),
            warranty_months=12,
            matching_confidence=Decimal("0.96"),
            match_reason="seed deterministic",
        )
        db.add(normalized)
        db.flush()

        history = PriceHistory(
            normalized_offer_id=normalized.id,
            item_price=Decimal("699.00"),
            shipping_price=Decimal("0.00"),
            effective_total_price=Decimal("699.00"),
            currency="CHF",
        )
        db.add(history)

        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed()
    print("seed complete")
