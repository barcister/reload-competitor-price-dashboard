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


class RefurbedCHConnector(BaseConnector):
    connector_key = "refurbed_ch"
    support_level = "FULL_SUPPORT"
    extraction_mode = "html_parse"

    async def discover_listing_urls(self) -> list[str]:
        return ["https://www.refurbed.example/ch/iphone-13"]

    async def fetch_listing(self, url: str) -> str:
        return (Path(__file__).parent / "fixtures" / "refurbed_product.html").read_text()

    def extract_raw_offer(self, payload: str | dict, source_url: str) -> list[dict]:
        offers = parse_jsonld_product_offers(str(payload), source_url)
        for offer in offers:
            offer["seller_name"] = "Marketplace Seller A"
            offer["shipping_price"] = 12
        return offers

    def normalize_offer(self, raw_offer: dict) -> dict:
        total, uncertain = effective_total_price(raw_offer["item_price"], raw_offer.get("shipping_price"))
        return {
            **raw_offer,
            "currency": normalize_currency(raw_offer["currency"]),
            "condition_grade": normalize_condition(raw_offer.get("condition_grade", "excellent")),
            "availability": normalize_availability(raw_offer.get("availability")),
            "battery_health_band": battery_health_band(raw_offer.get("battery_health_percent")),
            "effective_total_price": total,
            "effective_total_uncertain": uncertain,
        }

    def determine_capabilities(self) -> ConnectorCapabilities:
        return ConnectorCapabilities(True, False, True, True, True, False, True, True, True)

    def capture_snapshot(self, raw_payload: str, source_url: str) -> str | None:
        return f"snapshots/refurbed/{abs(hash(source_url))}.html"

    def validate_offer(self, normalized_offer: dict) -> bool:
        return normalized_offer.get("effective_total_price") is not None
