from services.matcher.app.matcher import PhoneMatcher


def test_matcher_returns_deterministic_match():
    matcher = PhoneMatcher()
    candidates = [
        {
            "id": 1,
            "model_name": "Iphone 14 Pro",
            "storage_gb": 128,
            "search_title": "Apple iPhone 14 Pro 128GB Space Gray",
        }
    ]
    result = matcher.match("Apple iPhone 14 Pro 128GB Space Gray", candidates)
    assert result.canonical_phone_id == 1
    assert result.match_confidence >= 0.9
