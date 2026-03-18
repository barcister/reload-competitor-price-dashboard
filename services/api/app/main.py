from fastapi import FastAPI

from services.api.app.routers.buyback_quotes import router as buyback_router
from services.api.app.routers.dashboard import router as dashboard_router
from services.api.app.routers.health import router as health_router
from services.api.app.routers.ingestion import router as ingestion_router
from services.api.app.routers.manual_review import router as manual_review_router
from services.api.app.routers.offers import router as offers_router
from services.api.app.routers.phones import router as phones_router
from services.api.app.routers.providers import router as providers_router

app = FastAPI(title="Swiss Phone Price Intelligence API", version="0.2.0")

app.include_router(health_router)
app.include_router(providers_router)
app.include_router(phones_router)
app.include_router(offers_router)
app.include_router(buyback_router)
app.include_router(manual_review_router)
app.include_router(ingestion_router)
app.include_router(dashboard_router)
