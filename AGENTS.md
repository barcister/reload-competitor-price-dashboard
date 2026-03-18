# AGENTS.md

Repository engineering guardrails:

1. Keep diffs scoped to the requested milestone; avoid opportunistic refactors.
2. Validate after each milestone (`make lint`, `make test`, targeted smoke checks).
3. Prefer simple, robust, deterministic implementations over clever abstractions.
4. Respect public-data collection constraints and never add anti-bot bypass logic.
5. Update docs (`README.md`, `docs/*`, `PLANS.md`) whenever behavior or structure changes.
6. If a connector cannot be made reliable from public pages, mark it `LIMITED_SUPPORT`.
7. Use typed schemas and explicit enums for provider/capability fields.
8. Keep architecture independent from ERP integrations.
