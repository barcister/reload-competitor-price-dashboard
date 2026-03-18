from pathlib import Path

from services.collector.app.base_adapter import BaseConnector, ConnectorCapabilities
from services.collector.app.jsonld_parser import parse_jsonld_product_offers
from services.common.utils.normalization import (
    battery_health_band,
    effective_total_price,
    normalize_availability,
    normalize_condition,
    normalize_currency,
)


class RevendoConnector(BaseConnector):
    connector_key = "revendo"
    support_level = "FULL_SUPPORT"
    extraction_mode = "structured_data"

    async def discover_listing_urls(self) -> list[str]:
        return ["https://www.revendo.example/ch/iphone-14"]

    async def fetch_listing(self, url: str) -> str:
        fixture = Path(__file__).parent / "fixtures" / "revendo_product.html"
        return fixture.read_text()

    def extract_raw_offer(self, payload: str | dict, source_url: str) -> list[dict]:
        return parse_jsonld_product_offers(str(payload), source_url)

    def normalize_offer(self, raw_offer: dict) -> dict:
        total, uncertain = effective_total_price(raw_offer["item_price"], None)
        return {
            **raw_offer,
            "currency": normalize_currency(raw_offer["currency"]),
            "condition_grade": normalize_condition(raw_offer.get("condition_grade")),
            "availability": normalize_availability(raw_offer.get("availability")),
            "battery_health_band": battery_health_band(raw_offer.get("battery_health_percent")),
            "effective_total_price": total,
            "effective_total_uncertain": uncertain,
        }

    def determine_capabilities(self) -> ConnectorCapabilities:
        return ConnectorCapabilities(True, False, True, False, True, False, True, True, True)

    def capture_snapshot(self, raw_payload: str, source_url: str) -> str | None:
        return f"snapshots/revendo/{abs(hash(source_url))}.html"

    def validate_offer(self, normalized_offer: dict) -> bool:
        return bool(normalized_offer.get("raw_title") and normalized_offer.get("item_price"))
