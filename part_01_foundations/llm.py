"""Part 1 — LLM factory: creates ChatOpenAI or ChatAnthropic from env config."""

from functools import lru_cache
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.language_models import BaseChatModel

from shared.config import get_settings


@lru_cache
def get_llm(streaming: bool = False) -> BaseChatModel:
    settings = get_settings()
    model = settings.llm_model

    if model.startswith("claude"):
        return ChatAnthropic(
            model=model,
            anthropic_api_key=settings.anthropic_api_key,
            streaming=streaming,
        )

    return ChatOpenAI(
        model=model,
        openai_api_key=settings.openai_api_key,
        streaming=streaming,
        temperature=0.7,
    )
