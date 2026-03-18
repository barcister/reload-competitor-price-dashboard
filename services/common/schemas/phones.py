from pydantic import BaseModel


class CanonicalPhoneCreate(BaseModel):
    brand: str
    model_family: str
    model_name: str
    storage_gb: int
    color: str | None = None
    condition_grade: str
    battery_health_percent: int | None = None
    network_lock_status: str | None = None
    dual_sim_or_esim: bool | None = None
    warranty_months: int | None = None
    sku: str | None = None
