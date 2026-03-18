from pathlib import Path

from services.collector.app.jsonld_parser import parse_jsonld_product_offers


def test_jsonld_parser_extracts_offer():
    html = (Path(__file__).resolve().parents[1] / "connectors" / "fixtures" / "revendo_product.html").read_text()
    offers = parse_jsonld_product_offers(html, "https://www.revendo.example/ch/iphone-14")
    assert len(offers) == 1
    assert str(offers[0]["item_price"]) == "699.00"
    assert offers[0]["currency"] == "CHF"
