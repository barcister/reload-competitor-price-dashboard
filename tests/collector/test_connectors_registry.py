from services.collector.app.registry import CONNECTOR_REGISTRY


def test_registry_has_required_connectors():
    assert "revendo" in CONNECTOR_REGISTRY
    assert "refurbed_ch" in CONNECTOR_REGISTRY
    assert "backmarket_ch" in CONNECTOR_REGISTRY
