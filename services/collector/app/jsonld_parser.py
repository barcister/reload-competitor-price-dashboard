import json
from decimal import Decimal

from bs4 import BeautifulSoup


def parse_jsonld_product_offers(html: str, source_url: str) -> list[dict]:
    soup = BeautifulSoup(html, "lxml")
    offers: list[dict] = []
    for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
        try:
            data = json.loads(script.string or "{}")
        except json.JSONDecodeError:
            continue
        nodes = data if isinstance(data, list) else [data]
        for node in nodes:
            if node.get("@type") != "Product":
                continue
            offer_node = node.get("offers") or {}
            if isinstance(offer_node, list):
                offer_node = offer_node[0]
            price = offer_node.get("price")
            if not price:
                continue
            offers.append(
                {
                    "source_url": source_url,
                    "raw_title": node.get("name", "unknown"),
                    "item_price": Decimal(str(price)),
                    "currency": offer_node.get("priceCurrency", "CHF"),
                    "availability": offer_node.get("availability"),
                    "raw_payload": node,
                    "extraction_confidence": 0.88,
                }
            )
    return offers
