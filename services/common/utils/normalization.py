import re
from decimal import Decimal

CONDITION_MAP = {
    "neu": "New",
    "new": "New",
    "wie neu": "Like New",
    "like new": "Like New",
    "sehr gut": "Excellent",
    "excellent": "Excellent",
    "gut": "Good",
    "good": "Good",
    "fair": "Fair",
    "befriedigend": "Fair",
}

COLOR_MAP = {
    "space grau": "Space Gray",
    "space gray": "Space Gray",
    "schwarz": "Black",
    "schwarz/midnight": "Midnight",
    "blau": "Blue",
}

CURRENCY_MAP = {"CHF": "CHF", "Fr.": "CHF", "SFR": "CHF", "$": "USD", "€": "EUR"}


def normalize_storage_to_gb(value: str) -> int | None:
    text = value.lower().replace(" ", "")
    gb_match = re.search(r"(\d+(?:\.\d+)?)gb", text)
    tb_match = re.search(r"(\d+(?:\.\d+)?)tb", text)
    if gb_match:
        return int(float(gb_match.group(1)))
    if tb_match:
        return int(float(tb_match.group(1)) * 1024)
    return None


def normalize_model_name(text: str) -> str:
    cleaned = re.sub(r"\bapple\b", "", text, flags=re.IGNORECASE).strip()
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.title()


def normalize_condition(value: str | None) -> str:
    if not value:
        return "Unknown"
    key = value.strip().lower()
    return CONDITION_MAP.get(key, "Unknown")


def normalize_color(value: str | None) -> str | None:
    if not value:
        return None
    key = value.strip().lower()
    return COLOR_MAP.get(key, value.title())


def normalize_currency(value: str) -> str:
    return CURRENCY_MAP.get(value.strip(), value.strip().upper())


def parse_battery_health_percent(text: str | None) -> int | None:
    if not text:
        return None
    match = re.search(r"(\d{2,3})\s*%", text)
    return int(match.group(1)) if match else None


def battery_health_band(percent: int | None) -> str:
    if percent is None:
        return "unknown"
    if percent >= 100:
        return "100"
    if percent >= 95:
        return "95_to_99"
    if percent >= 90:
        return "90_to_94"
    if percent >= 85:
        return "85_to_89"
    return "below_85"


def normalize_availability(value: str | None) -> str:
    if not value:
        return "unknown"
    lower = value.lower()
    if "in stock" in lower or "verfügbar" in lower:
        return "in_stock"
    if "out" in lower or "nicht" in lower:
        return "out_of_stock"
    return "unknown"


def effective_total_price(item_price: Decimal, shipping: Decimal | None) -> tuple[Decimal, bool]:
    if shipping is None:
        return (item_price, True)
    return (item_price + shipping, False)
