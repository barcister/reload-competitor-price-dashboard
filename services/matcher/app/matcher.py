import re
from dataclasses import dataclass

from rapidfuzz import fuzz

from services.common.utils.normalization import normalize_model_name, normalize_storage_to_gb


@dataclass
class MatchResult:
    canonical_phone_id: int | None
    match_confidence: float
    match_reason: str
    ambiguous_fields: list[str]


class PhoneMatcher:
    def parse_title(self, title: str) -> dict:
        lower = title.lower()
        storage = normalize_storage_to_gb(title)
        model_match = re.search(r"(iphone\s?\d+\s?(?:pro|max|plus)?)", lower)
        model = normalize_model_name(model_match.group(1) if model_match else title)
        return {"model": model, "storage_gb": storage}

    def match(self, raw_title: str, candidates: list[dict]) -> MatchResult:
        parsed = self.parse_title(raw_title)
        ambiguous_fields = []

        if parsed["storage_gb"] is None:
            ambiguous_fields.append("storage_gb")

        for candidate in candidates:
            if (
                candidate["model_name"].lower() == parsed["model"].lower()
                and candidate["storage_gb"] == parsed["storage_gb"]
            ):
                return MatchResult(candidate["id"], 0.96, "deterministic model+storage", ambiguous_fields)

        best = None
        best_score = 0
        for candidate in candidates:
            score = fuzz.token_set_ratio(raw_title.lower(), candidate["search_title"].lower())
            if score > best_score:
                best_score = score
                best = candidate

        if best and best_score >= 86:
            return MatchResult(best["id"], round(best_score / 100, 3), "fuzzy title similarity", ambiguous_fields)

        ambiguous_fields.extend(["model_name", "storage_gb"])
        return MatchResult(None, round(best_score / 100, 3), "manual review required", list(set(ambiguous_fields)))
