from decimal import Decimal


def to_decimal(value: str | int | float | Decimal) -> Decimal:
    return value if isinstance(value, Decimal) else Decimal(str(value))
