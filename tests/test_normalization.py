from services.common.utils.normalization import (
    battery_health_band,
    normalize_condition,
    normalize_storage_to_gb,
)


def test_storage_normalization():
    assert normalize_storage_to_gb("128GB") == 128
    assert normalize_storage_to_gb("1 TB") == 1024


def test_condition_map():
    assert normalize_condition("wie neu") == "Like New"


def test_battery_bands():
    assert battery_health_band(97) == "95_to_99"
    assert battery_health_band(None) == "unknown"
