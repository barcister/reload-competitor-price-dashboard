# Connectors

## Interface contract
Each connector implements:
- `discover_listing_urls()`
- `fetch_listing(url)`
- `extract_raw_offer(payload, source_url)`
- `normalize_offer(raw_offer)`
- `determine_capabilities()`
- `capture_snapshot(raw_payload, source_url)`
- `validate_offer(normalized_offer)`

## Support levels
- `FULL_SUPPORT`: stable public extraction working end-to-end.
- `PARTIAL_SUPPORT`: usable with caveats (missing fields or occasional dynamic blockers).
- `LIMITED_SUPPORT`: publicly accessible data insufficient for robust extraction.

## Implemented examples
- `revendo` (FULL_SUPPORT)
- `refurbed_ch` (FULL_SUPPORT)
- `backmarket_ch` (FULL_SUPPORT)

## Scaffolded examples
- `digitec_secondhand` (PARTIAL_SUPPORT scaffold)
- `galaxus_refurbished` (PARTIAL_SUPPORT scaffold)
- `mediamarkt_refurbished` (LIMITED_SUPPORT scaffold)
