"""Part 12 — LangSmith tracing setup and configuration."""

import os
from functools import wraps
from typing import Callable, Any


def configure_langsmith(
    project_name: str = "hospital-intelligence-platform",
    enabled: bool | None = None,
) -> bool:
    """Configure LangSmith tracing.

    If *enabled* is None, it is inferred from the LANGCHAIN_TRACING_V2
    environment variable.

    Returns True if tracing was successfully configured.
    """
    if enabled is None:
        enabled = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"

    if not enabled:
        return False

    api_key = os.getenv("LANGCHAIN_API_KEY")
    if not api_key:
        import warnings
        warnings.warn("LANGCHAIN_API_KEY not set — LangSmith tracing disabled.")
        return False

    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_PROJECT"] = project_name
    return True


def traced(name: str | None = None, tags: list[str] | None = None):
    """Decorator that adds run metadata to a traced LangChain function.

    Usage::

        @traced(name="triage_classify", tags=["triage", "classification"])
        async def classify(state):
            ...
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args, **kwargs) -> Any:
            return await func(*args, **kwargs)

        @wraps(func)
        def sync_wrapper(*args, **kwargs) -> Any:
            return func(*args, **kwargs)

        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper

    return decorator


def get_run_url(run_id: str) -> str:
    """Return the LangSmith UI URL for a specific run."""
    project = os.getenv("LANGCHAIN_PROJECT", "default")
    return f"https://smith.langchain.com/o/default/projects/p/{project}/r/{run_id}"
