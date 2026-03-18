from services.collector.app.base_adapter import BaseConnector, ConnectorCapabilities


class DigitecSecondhandConnector(BaseConnector):
    connector_key = "digitec_secondhand"
    support_level = "PARTIAL_SUPPORT"

    async def discover_listing_urls(self) -> list[str]:
        return []

    async def fetch_listing(self, url: str) -> str | dict:
        return ""

    def extract_raw_offer(self, payload: str | dict, source_url: str) -> list[dict]:
        # TODO: implement robust extraction from public second-hand listing pages.
        return []

    def normalize_offer(self, raw_offer: dict) -> dict:
        return raw_offer

    def determine_capabilities(self) -> ConnectorCapabilities:
        return ConnectorCapabilities(True, False, True, True, True, False, True, True, True)

    def capture_snapshot(self, raw_payload: str, source_url: str) -> str | None:
        return None

    def validate_offer(self, normalized_offer: dict) -> bool:
        return False
