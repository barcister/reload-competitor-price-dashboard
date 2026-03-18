# Architecture

```mermaid
flowchart LR
  subgraph Sources[Swiss Public Sources]
    A[Revendo]
    B[refurbed.ch]
    C[Back Market CH]
    D[Other listing/buyback/anchor sources]
  end

  subgraph Collector[services/collector]
    CR[Connector Registry]
    BC[Base Connector Interface]
    EX[Extraction fallback\nAPI/feed -> JSON-LD -> HTML -> Playwright]
    SNAP[Snapshot Capture]
  end

  subgraph Core[Core Services]
    MA[services/matcher]
    API[services/api]
  end

  subgraph Data[State]
    PG[(PostgreSQL)]
    REDIS[(Redis)]
    S3[(S3-compatible snapshots)]
  end

  subgraph UI[Internal Consumers]
    WEB[apps/web dashboard]
    BI[Future ERP / BI consumers]
  end

  Sources --> Collector
  Collector --> PG
  Collector --> REDIS
  Collector --> S3
  PG --> MA
  MA --> PG
  API --> PG
  API --> REDIS
  WEB --> API
  BI --> API
```

## Schema summary

Main entities:
- providers / provider_configs
- scrape_runs / scrape_errors / connector_health_snapshots
- raw_offers / normalized_offers / price_history
- canonical_phones / manual_match_reviews
- buyback_quotes
