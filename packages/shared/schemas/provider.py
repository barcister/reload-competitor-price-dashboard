from pydantic import BaseModel


class ProviderCapabilitySchema(BaseModel):
    supports_sell_price: bool
    supports_buyback_quote: bool
    supports_history: bool
    supports_marketplace_seller_identity: bool
    supports_condition_grade: bool
    supports_battery_health: bool
    supports_warranty: bool
    supports_shipping: bool
    supports_variant_level_matching: bool
