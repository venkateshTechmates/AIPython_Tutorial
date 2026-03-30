"""Part 1 — Health check router."""

from fastapi import APIRouter
from part_01_foundations.schemas import HealthResponse
from shared.config import get_settings

router = APIRouter(tags=["Health"])
settings = get_settings()


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    return HealthResponse(
        status="healthy",
        llm_model=settings.llm_model,
        environment=settings.environment,
    )
