"""Part 4 — OpenAI embedding model wrapper."""

from functools import lru_cache
from langchain_openai import OpenAIEmbeddings
from shared.config import get_settings


@lru_cache
def get_embeddings() -> OpenAIEmbeddings:
    settings = get_settings()
    return OpenAIEmbeddings(
        model=settings.embedding_model,
        openai_api_key=settings.openai_api_key,
    )
