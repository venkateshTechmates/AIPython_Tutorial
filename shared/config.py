"""Central configuration using Pydantic BaseSettings."""

from functools import lru_cache
from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ── LLM ───────────────────────────────────────────────────
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    llm_model: str = "gpt-4o"
    embedding_model: str = "text-embedding-3-small"

    # ── Qdrant ────────────────────────────────────────────────
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "hospital_docs"
    qdrant_api_key: str = ""

    # ── Database ──────────────────────────────────────────────
    database_url: str = "sqlite+aiosqlite:///./hospital.db"

    # ── LangSmith ─────────────────────────────────────────────
    langchain_tracing_v2: bool = False
    langchain_api_key: str = ""
    langchain_project: str = "hospital-ai"
    langchain_endpoint: str = "https://api.smith.langchain.com"

    # ── Application ───────────────────────────────────────────
    environment: str = "development"
    log_level: str = "INFO"
    secret_key: str = "change-me-in-production"
    allowed_origins: str = "http://localhost:3000,http://localhost:8000"

    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def is_production(self) -> bool:
        return self.environment == "production"

    @property
    def origins_list(self) -> list[str]:
        return [o.strip() for o in self.allowed_origins.split(",")]


@lru_cache
def get_settings() -> Settings:
    return Settings()
