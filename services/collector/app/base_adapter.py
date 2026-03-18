from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class ConnectorCapabilities:
    supports_sell_price: bool
    supports_buyback_quote: bool
    supports_history: bool
    supports_marketplace_seller_identity: bool
    supports_condition_grade: bool
    supports_battery_health: bool
    supports_warranty: bool
    supports_shipping: bool
    supports_variant_level_matching: bool


class BaseConnector(ABC):
    connector_key: str
    support_level: str = "PARTIAL_SUPPORT"
    extraction_mode: str = "structured_data"

    @abstractmethod
    async def discover_listing_urls(self) -> list[str]:
        pass

    @abstractmethod
    async def fetch_listing(self, url: str) -> str | dict[str, Any]:
        pass

    @abstractmethod
    def extract_raw_offer(self, payload: str | dict[str, Any], source_url: str) -> list[dict[str, Any]]:
        pass

    @abstractmethod
    def normalize_offer(self, raw_offer: dict[str, Any]) -> dict[str, Any]:
        pass

    @abstractmethod
    def determine_capabilities(self) -> ConnectorCapabilities:
        pass

    @abstractmethod
    def capture_snapshot(self, raw_payload: str, source_url: str) -> str | None:
        pass

    @abstractmethod
    def validate_offer(self, normalized_offer: dict[str, Any]) -> bool:
        pass
