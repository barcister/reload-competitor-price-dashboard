from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "phone-price-intel"
    environment: str = "dev"
    database_url: str = "postgresql+psycopg://postgres:postgres@postgres:5432/priceintel"
    redis_url: str = "redis://redis:6379/0"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    s3_bucket: str = "snapshots"
    s3_endpoint_url: str = "http://minio:9000"
    s3_access_key: str = "minio"
    s3_secret_key: str = "minio123"
    crawl_user_agent: str = "PriceIntelBot/1.0 (+internal competitive intelligence)"
    stale_offer_hours: int = 24
    primary_currency: str = "CHF"


settings = Settings()
