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


class BackMarketCHConnector(BaseConnector):
    connector_key = "backmarket_ch"
    support_level = "FULL_SUPPORT"
    extraction_mode = "browser_interaction"

    async def discover_listing_urls(self) -> list[str]:
        return ["https://www.backmarket.example/ch/apple-iphone-15"]

    async def fetch_listing(self, url: str) -> str:
        return (Path(__file__).parent / "fixtures" / "backmarket_product.html").read_text()

    def extract_raw_offer(self, payload: str | dict, source_url: str) -> list[dict]:
        return parse_jsonld_product_offers(str(payload), source_url)

    def normalize_offer(self, raw_offer: dict) -> dict:
        shipping = raw_offer.get("shipping_price", 0)
        total, uncertain = effective_total_price(raw_offer["item_price"], shipping)
        return {
            **raw_offer,
            "currency": normalize_currency(raw_offer["currency"]),
            "condition_grade": normalize_condition(raw_offer.get("condition_grade", "good")),
            "availability": normalize_availability(raw_offer.get("availability")),
            "battery_health_band": battery_health_band(raw_offer.get("battery_health_percent")),
            "effective_total_price": total,
            "effective_total_uncertain": uncertain,
        }

    def determine_capabilities(self) -> ConnectorCapabilities:
        return ConnectorCapabilities(True, False, True, True, True, True, True, True, True)

    def capture_snapshot(self, raw_payload: str, source_url: str) -> str | None:
        return f"snapshots/backmarket/{abs(hash(source_url))}.html"

    def validate_offer(self, normalized_offer: dict) -> bool:
        return normalized_offer.get("currency") == "CHF"
