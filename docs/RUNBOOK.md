# RUNBOOK: Running the Swiss Phone Price Intelligence MVP

This runbook explains how to start, migrate, seed, and verify the stack locally.

## 1) Prerequisites

### Required
- Docker Engine + Docker Compose plugin
- Python 3.11+ (if running API outside Docker)
- GNU Make

### Optional (for web local dev outside Docker)
- Node.js 20+
- npm 10+

---

## 2) Environment configuration

1. Copy the sample env file:
   ```bash
   cp .env.example .env
   ```
2. Review these critical values in `.env`:
   - `DATABASE_URL`
   - `REDIS_URL`
   - `NEXT_PUBLIC_API_BASE`
   - `PRIMARY_CURRENCY`

> Default values are preconfigured for local Docker networking.

---

## 3) Quick start (recommended)

From repository root:

```bash
make dev
```

Equivalent command:

```bash
docker compose up --build
```

This starts:
- postgres
- redis
- api
- collector
- scheduler
- web

---

## 4) Database migration and seed data

With containers running:

```bash
make migrate
make seed
```

Equivalent direct commands:

```bash
alembic upgrade head
python scripts/seed_data.py
```

> If you run migration/seed inside the API container, use:
> `docker compose exec api alembic upgrade head` and
> `docker compose exec api python scripts/seed_data.py`.

---

## 5) Access points

- API OpenAPI docs: http://localhost:8000/docs
- API health: http://localhost:8000/health
- Web dashboard: http://localhost:3000

---

## 6) Functional smoke test

After seed:

```bash
curl http://localhost:8000/health
curl http://localhost:8000/providers
curl http://localhost:8000/phones
curl http://localhost:8000/dashboard/summary
curl -X POST http://localhost:8000/ingestion/run -H 'content-type: application/json' -d '{"connectors":["revendo","refurbed_ch","backmarket_ch"]}'
```

Expected outcomes:
- `/health` returns `{"status":"ok"}`
- `/providers` and `/phones` return seeded lists
- `/dashboard/summary` returns counts
- ingestion returns connector run metrics

---

## 7) Running tests and lint

```bash
make lint
make test
```

Notes:
- In network-restricted environments, dependency installation may fail.
- If so, prefer Docker-based execution where dependencies are baked into images.

---

## 8) Running services individually (advanced)

### API only (local Python)
```bash
make setup
make migrate
make seed
uvicorn services.api.app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Web only (local Node)
```bash
cd apps/web
npm install
NEXT_PUBLIC_API_BASE=http://localhost:8000 npm run dev
```

---

## 9) Troubleshooting

### API cannot connect to Postgres
- Verify `postgres` container is running: `docker compose ps`
- Confirm `DATABASE_URL` matches local service hostname/port.

### Web cannot load API data
- Ensure `NEXT_PUBLIC_API_BASE` points to reachable API URL.
- Check browser dev tools network tab for 4xx/5xx responses.

### Migration errors
- Ensure alembic points to correct DB in `alembic.ini` and `.env`.
- If local DB state is broken, recreate containers/volumes:
  ```bash
  docker compose down -v
  docker compose up --build
  ```

### Collector returns zero offers
- Run ingestion manually for implemented connectors:
  `POST /ingestion/run` with `revendo`, `refurbed_ch`, `backmarket_ch`.
- Validate fixture files still exist and parser tests pass.

---

## 10) Production-minded notes

- Public data only; no login/cart/checkout/captcha flows.
- Unsupported dynamic providers should remain `PARTIAL_SUPPORT` or `LIMITED_SUPPORT`.
- Keep schema changes behind Alembic migrations.
- Update `PLANS.md` and `docs/*` whenever behavior changes.
