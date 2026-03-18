from fastapi import APIRouter
from pydantic import BaseModel

from services.collector.app.runner import run_ingestion

router = APIRouter(prefix="/ingestion", tags=["ingestion"])


class IngestionPayload(BaseModel):
    connectors: list[str] | None = None


@router.post("/run")
async def run(payload: IngestionPayload):
    return await run_ingestion(payload.connectors)
