from services.matcher.app.matcher import PhoneMatcher


def run_match(raw_title: str, candidates: list[dict]) -> dict:
    result = PhoneMatcher().match(raw_title, candidates)
    return {
        "canonical_phone_id": result.canonical_phone_id,
        "match_confidence": result.match_confidence,
        "match_reason": result.match_reason,
        "ambiguous_fields": result.ambiguous_fields,
    }
