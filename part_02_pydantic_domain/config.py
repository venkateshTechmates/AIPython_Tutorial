"""Part 2 — Pydantic BaseSettings configuration."""

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    llm_model: str = "gpt-4o"
    environment: str = "development"
    log_level: str = "INFO"

    model_config = ConfigDict(env_file=".env", extra="ignore")


def get_settings() -> Settings:
    return Settings()
