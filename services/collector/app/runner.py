import asyncio
from datetime import datetime

from services.collector.app.registry import CONNECTOR_REGISTRY


async def run_ingestion(connector_keys: list[str] | None = None) -> dict:
    selected = connector_keys or list(CONNECTOR_REGISTRY.keys())
    result = {"started_at": datetime.utcnow().isoformat(), "connectors": []}
    for key in selected:
        connector = CONNECTOR_REGISTRY[key]()
        urls = await connector.discover_listing_urls()
        pages_fetched = 0
        extracted = 0
        for url in urls:
            payload = await connector.fetch_listing(url)
            raw_offers = connector.extract_raw_offer(payload, url)
            extracted += len(raw_offers)
            pages_fetched += 1
        result["connectors"].append(
            {
                "connector": key,
                "support_level": connector.support_level,
                "pages_fetched": pages_fetched,
                "offers_extracted": extracted,
            }
        )
    result["finished_at"] = datetime.utcnow().isoformat()
    return result


if __name__ == "__main__":
    print(asyncio.run(run_ingestion()))
