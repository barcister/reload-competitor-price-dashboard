"""init schema"""

from alembic import op
import sqlalchemy as sa

revision = "0001_init"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "providers",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("storefront_name", sa.String(150), nullable=False, unique=True),
        sa.Column("underlying_provider_name", sa.String(150), nullable=True),
        sa.Column("provider_type", sa.String(50), nullable=False),
        sa.Column("automation_level", sa.String(30), nullable=False),
        sa.Column("reliability_score", sa.Numeric(4, 2), nullable=False),
        sa.Column("reliability_status", sa.String(30), nullable=False),
        sa.Column("supports_sell_price", sa.Boolean(), nullable=False),
        sa.Column("supports_buyback_quote", sa.Boolean(), nullable=False),
        sa.Column("supports_history", sa.Boolean(), nullable=False),
        sa.Column("supports_marketplace_seller_identity", sa.Boolean(), nullable=False),
        sa.Column("supports_condition_grade", sa.Boolean(), nullable=False),
        sa.Column("supports_battery_health", sa.Boolean(), nullable=False),
        sa.Column("supports_warranty", sa.Boolean(), nullable=False),
        sa.Column("supports_shipping", sa.Boolean(), nullable=False),
        sa.Column("supports_variant_level_matching", sa.Boolean(), nullable=False),
        sa.Column("support_level", sa.String(20), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "provider_configs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("provider_id", sa.Integer(), sa.ForeignKey("providers.id"), nullable=False),
        sa.Column("connector_key", sa.String(100), nullable=False, unique=True),
        sa.Column("base_url", sa.String(500), nullable=False),
        sa.Column("priority", sa.Integer(), nullable=False),
        sa.Column("compare_mode", sa.String(50), nullable=False),
        sa.Column("extraction_mode", sa.String(50), nullable=False),
        sa.Column("robots_enabled", sa.Boolean(), nullable=False),
        sa.Column("crawl_delay_seconds", sa.Integer(), nullable=False),
        sa.Column("request_timeout_seconds", sa.Integer(), nullable=False),
        sa.Column("rate_limit_per_minute", sa.Integer(), nullable=False),
    )

    op.create_table(
        "canonical_phones",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("brand", sa.String(80), nullable=False),
        sa.Column("model_family", sa.String(120), nullable=False),
        sa.Column("model_name", sa.String(160), nullable=False),
        sa.Column("generation", sa.String(60), nullable=True),
        sa.Column("storage_gb", sa.Integer(), nullable=False),
        sa.Column("color", sa.String(80), nullable=True),
        sa.Column("condition_grade", sa.String(40), nullable=False),
        sa.Column("battery_health_percent", sa.Integer(), nullable=True),
        sa.Column("battery_health_band", sa.String(40), nullable=False),
        sa.Column("network_lock_status", sa.String(50), nullable=True),
        sa.Column("sim_type", sa.String(40), nullable=True),
        sa.Column("dual_sim_or_esim", sa.Boolean(), nullable=True),
        sa.Column("warranty_months", sa.Integer(), nullable=True),
        sa.Column("region_or_sku", sa.String(120), nullable=True),
        sa.Column("release_year", sa.Integer(), nullable=True),
    )

    op.create_table(
        "scrape_runs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("provider_id", sa.Integer(), sa.ForeignKey("providers.id"), nullable=False),
        sa.Column("connector_key", sa.String(100), nullable=False),
        sa.Column("started_at", sa.DateTime(), nullable=False),
        sa.Column("finished_at", sa.DateTime(), nullable=True),
        sa.Column("pages_fetched", sa.Integer(), nullable=False),
        sa.Column("offers_extracted", sa.Integer(), nullable=False),
        sa.Column("offers_normalized", sa.Integer(), nullable=False),
        sa.Column("offers_matched", sa.Integer(), nullable=False),
        sa.Column("low_confidence_matches", sa.Integer(), nullable=False),
        sa.Column("failed_pages", sa.Integer(), nullable=False),
        sa.Column("connector_success_ratio", sa.Numeric(5, 2), nullable=False),
        sa.Column("status", sa.String(30), nullable=False),
    )

    op.create_table(
        "scrape_errors",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("scrape_run_id", sa.Integer(), sa.ForeignKey("scrape_runs.id"), nullable=False),
        sa.Column("source_url", sa.String(600), nullable=True),
        sa.Column("error_type", sa.String(100), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("raw_snapshot_path", sa.String(500), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "raw_offers",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("provider_id", sa.Integer(), sa.ForeignKey("providers.id"), nullable=False),
        sa.Column("source_url", sa.String(600), nullable=False),
        sa.Column("source_identifier", sa.String(180), nullable=True),
        sa.Column("raw_title", sa.String(600), nullable=False),
        sa.Column("seller_name", sa.String(140), nullable=True),
        sa.Column("extraction_mode", sa.String(40), nullable=False),
        sa.Column("extraction_confidence", sa.Numeric(4, 3), nullable=False),
        sa.Column("raw_snapshot_path", sa.String(500), nullable=True),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("scraped_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "normalized_offers",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("raw_offer_id", sa.Integer(), sa.ForeignKey("raw_offers.id"), nullable=False),
        sa.Column("canonical_phone_id", sa.Integer(), sa.ForeignKey("canonical_phones.id"), nullable=True),
        sa.Column("normalized_title", sa.String(600), nullable=False),
        sa.Column("item_price", sa.Numeric(10, 2), nullable=False),
        sa.Column("shipping_price", sa.Numeric(10, 2), nullable=True),
        sa.Column("effective_total_price", sa.Numeric(10, 2), nullable=True),
        sa.Column("effective_total_uncertain", sa.Boolean(), nullable=False),
        sa.Column("currency", sa.String(3), nullable=False),
        sa.Column("availability", sa.String(50), nullable=True),
        sa.Column("condition_grade", sa.String(40), nullable=False),
        sa.Column("battery_health_percent", sa.Integer(), nullable=True),
        sa.Column("battery_health_band", sa.String(40), nullable=False),
        sa.Column("warranty_months", sa.Integer(), nullable=True),
        sa.Column("matching_confidence", sa.Numeric(4, 3), nullable=True),
        sa.Column("match_reason", sa.Text(), nullable=True),
        sa.Column("comparability_warning", sa.Text(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "price_history",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("normalized_offer_id", sa.Integer(), sa.ForeignKey("normalized_offers.id"), nullable=False),
        sa.Column("item_price", sa.Numeric(10, 2), nullable=False),
        sa.Column("shipping_price", sa.Numeric(10, 2), nullable=True),
        sa.Column("effective_total_price", sa.Numeric(10, 2), nullable=True),
        sa.Column("currency", sa.String(3), nullable=False),
        sa.Column("captured_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "manual_match_reviews",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("normalized_offer_id", sa.Integer(), sa.ForeignKey("normalized_offers.id"), nullable=False),
        sa.Column("proposed_canonical_phone_id", sa.Integer(), sa.ForeignKey("canonical_phones.id"), nullable=True),
        sa.Column("ambiguous_fields", sa.JSON(), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("status", sa.String(30), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("resolved_at", sa.DateTime(), nullable=True),
    )

    op.create_table(
        "buyback_quotes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("provider_id", sa.Integer(), sa.ForeignKey("providers.id"), nullable=False),
        sa.Column("canonical_phone_id", sa.Integer(), sa.ForeignKey("canonical_phones.id"), nullable=True),
        sa.Column("source_url", sa.String(600), nullable=False),
        sa.Column("quoted_price", sa.Numeric(10, 2), nullable=False),
        sa.Column("currency", sa.String(3), nullable=False),
        sa.Column("condition_grade", sa.String(40), nullable=True),
        sa.Column("quote_context", sa.JSON(), nullable=False),
        sa.Column("scraped_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "connector_health_snapshots",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("provider_id", sa.Integer(), sa.ForeignKey("providers.id"), nullable=False),
        sa.Column("connector_key", sa.String(100), nullable=False),
        sa.Column("checked_at", sa.DateTime(), nullable=False),
        sa.Column("status", sa.String(30), nullable=False),
        sa.Column("message", sa.String(500), nullable=True),
        sa.Column("pages_fetched", sa.Integer(), nullable=False),
        sa.Column("offers_extracted", sa.Integer(), nullable=False),
        sa.Column("parse_failures", sa.Integer(), nullable=False),
    )


def downgrade() -> None:
    for table in [
        "connector_health_snapshots",
        "buyback_quotes",
        "manual_match_reviews",
        "price_history",
        "normalized_offers",
        "raw_offers",
        "scrape_errors",
        "scrape_runs",
        "canonical_phones",
        "provider_configs",
        "providers",
    ]:
        op.drop_table(table)
