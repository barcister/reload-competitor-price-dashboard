from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from services.common.db.base import Base


class Provider(Base):
    __tablename__ = "providers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    storefront_name: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    underlying_provider_name: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    provider_type: Mapped[str] = mapped_column(String(50), nullable=False)
    automation_level: Mapped[str] = mapped_column(String(30), nullable=False)
    reliability_score: Mapped[Decimal] = mapped_column(Numeric(4, 2), default=0.5)
    reliability_status: Mapped[str] = mapped_column(String(30), default="unknown")
    supports_sell_price: Mapped[bool] = mapped_column(Boolean, default=True)
    supports_buyback_quote: Mapped[bool] = mapped_column(Boolean, default=False)
    supports_history: Mapped[bool] = mapped_column(Boolean, default=True)
    supports_marketplace_seller_identity: Mapped[bool] = mapped_column(Boolean, default=False)
    supports_condition_grade: Mapped[bool] = mapped_column(Boolean, default=True)
    supports_battery_health: Mapped[bool] = mapped_column(Boolean, default=False)
    supports_warranty: Mapped[bool] = mapped_column(Boolean, default=False)
    supports_shipping: Mapped[bool] = mapped_column(Boolean, default=True)
    supports_variant_level_matching: Mapped[bool] = mapped_column(Boolean, default=True)
    support_level: Mapped[str] = mapped_column(String(20), default="PARTIAL_SUPPORT")
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ProviderConfig(Base):
    __tablename__ = "provider_configs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    provider_id: Mapped[int] = mapped_column(ForeignKey("providers.id"), nullable=False)
    connector_key: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    base_url: Mapped[str] = mapped_column(String(500), nullable=False)
    priority: Mapped[int] = mapped_column(Integer, default=1)
    compare_mode: Mapped[str] = mapped_column(String(50), nullable=False)
    extraction_mode: Mapped[str] = mapped_column(String(50), nullable=False)
    robots_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    crawl_delay_seconds: Mapped[int] = mapped_column(Integer, default=2)
    request_timeout_seconds: Mapped[int] = mapped_column(Integer, default=20)
    rate_limit_per_minute: Mapped[int] = mapped_column(Integer, default=30)


class ScrapeRun(Base):
    __tablename__ = "scrape_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    provider_id: Mapped[int] = mapped_column(ForeignKey("providers.id"), nullable=False)
    connector_key: Mapped[str] = mapped_column(String(100), nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    pages_fetched: Mapped[int] = mapped_column(Integer, default=0)
    offers_extracted: Mapped[int] = mapped_column(Integer, default=0)
    offers_normalized: Mapped[int] = mapped_column(Integer, default=0)
    offers_matched: Mapped[int] = mapped_column(Integer, default=0)
    low_confidence_matches: Mapped[int] = mapped_column(Integer, default=0)
    failed_pages: Mapped[int] = mapped_column(Integer, default=0)
    connector_success_ratio: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=0)
    status: Mapped[str] = mapped_column(String(30), default="running")


class ScrapeError(Base):
    __tablename__ = "scrape_errors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    scrape_run_id: Mapped[int] = mapped_column(ForeignKey("scrape_runs.id"), nullable=False)
    source_url: Mapped[Optional[str]] = mapped_column(String(600), nullable=True)
    error_type: Mapped[str] = mapped_column(String(100), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    raw_snapshot_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class CanonicalPhone(Base):
    __tablename__ = "canonical_phones"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    brand: Mapped[str] = mapped_column(String(80), nullable=False)
    model_family: Mapped[str] = mapped_column(String(120), nullable=False)
    model_name: Mapped[str] = mapped_column(String(160), nullable=False)
    generation: Mapped[Optional[str]] = mapped_column(String(60), nullable=True)
    storage_gb: Mapped[int] = mapped_column(Integer, nullable=False)
    color: Mapped[Optional[str]] = mapped_column(String(80), nullable=True)
    condition_grade: Mapped[str] = mapped_column(String(40), nullable=False, default="Unknown")
    battery_health_percent: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    battery_health_band: Mapped[str] = mapped_column(String(40), default="unknown")
    network_lock_status: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    sim_type: Mapped[Optional[str]] = mapped_column(String(40), nullable=True)
    dual_sim_or_esim: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    warranty_months: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    region_or_sku: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    release_year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)


class RawOffer(Base):
    __tablename__ = "raw_offers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    provider_id: Mapped[int] = mapped_column(ForeignKey("providers.id"), nullable=False)
    source_url: Mapped[str] = mapped_column(String(600), nullable=False)
    source_identifier: Mapped[Optional[str]] = mapped_column(String(180), nullable=True)
    raw_title: Mapped[str] = mapped_column(String(600), nullable=False)
    seller_name: Mapped[Optional[str]] = mapped_column(String(140), nullable=True)
    extraction_mode: Mapped[str] = mapped_column(String(40), nullable=False)
    extraction_confidence: Mapped[Decimal] = mapped_column(Numeric(4, 3), default=0.6)
    raw_snapshot_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    payload: Mapped[dict] = mapped_column(JSON, default={})
    scraped_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class NormalizedOffer(Base):
    __tablename__ = "normalized_offers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    raw_offer_id: Mapped[int] = mapped_column(ForeignKey("raw_offers.id"), nullable=False)
    canonical_phone_id: Mapped[Optional[int]] = mapped_column(ForeignKey("canonical_phones.id"), nullable=True)
    normalized_title: Mapped[str] = mapped_column(String(600), nullable=False)
    item_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    shipping_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2), nullable=True)
    effective_total_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2), nullable=True)
    effective_total_uncertain: Mapped[bool] = mapped_column(Boolean, default=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    availability: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    condition_grade: Mapped[str] = mapped_column(String(40), default="Unknown")
    battery_health_percent: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    battery_health_band: Mapped[str] = mapped_column(String(40), default="unknown")
    warranty_months: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    matching_confidence: Mapped[Optional[Decimal]] = mapped_column(Numeric(4, 3), nullable=True)
    match_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    comparability_warning: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class PriceHistory(Base):
    __tablename__ = "price_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    normalized_offer_id: Mapped[int] = mapped_column(ForeignKey("normalized_offers.id"), nullable=False)
    item_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    shipping_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2), nullable=True)
    effective_total_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2), nullable=True)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    captured_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ManualMatchReview(Base):
    __tablename__ = "manual_match_reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    normalized_offer_id: Mapped[int] = mapped_column(ForeignKey("normalized_offers.id"), nullable=False)
    proposed_canonical_phone_id: Mapped[Optional[int]] = mapped_column(ForeignKey("canonical_phones.id"), nullable=True)
    ambiguous_fields: Mapped[list] = mapped_column(JSON, default=[])
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)


class BuybackQuote(Base):
    __tablename__ = "buyback_quotes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    provider_id: Mapped[int] = mapped_column(ForeignKey("providers.id"), nullable=False)
    canonical_phone_id: Mapped[Optional[int]] = mapped_column(ForeignKey("canonical_phones.id"), nullable=True)
    source_url: Mapped[str] = mapped_column(String(600), nullable=False)
    quoted_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    condition_grade: Mapped[Optional[str]] = mapped_column(String(40), nullable=True)
    quote_context: Mapped[dict] = mapped_column(JSON, default={})
    scraped_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ConnectorHealthSnapshot(Base):
    __tablename__ = "connector_health_snapshots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    provider_id: Mapped[int] = mapped_column(ForeignKey("providers.id"), nullable=False)
    connector_key: Mapped[str] = mapped_column(String(100), nullable=False)
    checked_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    message: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    pages_fetched: Mapped[int] = mapped_column(Integer, default=0)
    offers_extracted: Mapped[int] = mapped_column(Integer, default=0)
    parse_failures: Mapped[int] = mapped_column(Integer, default=0)
