from services.collector.app.base_adapter import BaseConnector, ConnectorCapabilities


class MediaMarktRefurbishedConnector(BaseConnector):
    connector_key = "mediamarkt_refurbished"
    support_level = "LIMITED_SUPPORT"

    async def discover_listing_urls(self) -> list[str]:
        return []

    async def fetch_listing(self, url: str) -> str | dict:
        return ""

    def extract_raw_offer(self, payload: str | dict, source_url: str) -> list[dict]:
        # TODO: provider public pages currently unstable for robust extraction.
        return []

    def normalize_offer(self, raw_offer: dict) -> dict:
        return raw_offer

    def determine_capabilities(self) -> ConnectorCapabilities:
        return ConnectorCapabilities(True, False, True, False, True, False, True, True, True)

    def capture_snapshot(self, raw_payload: str, source_url: str) -> str | None:
        return None

    def validate_offer(self, normalized_offer: dict) -> bool:
        return False
