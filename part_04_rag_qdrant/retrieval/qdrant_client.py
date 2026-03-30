"""Part 4 — Qdrant client singleton."""

from functools import lru_cache
from qdrant_client import QdrantClient
from shared.config import get_settings


@lru_cache
def get_client() -> QdrantClient:
    settings = get_settings()
    return QdrantClient(
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key or None,
    )
