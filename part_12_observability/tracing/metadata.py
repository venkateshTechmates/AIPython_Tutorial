"""Part 12 — Request metadata injection for LangSmith traces."""

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult


class MetadataCallbackHandler(BaseCallbackHandler):
    """Attach structured metadata to every LLM invocation for observability.

    This handler injects:
    - session_id
    - patient_id (if provided)
    - endpoint / workflow name
    - environment
    """

    def __init__(
        self,
        session_id: str,
        patient_id: str | None = None,
        workflow: str = "unknown",
        environment: str = "development",
    ) -> None:
        self.session_id = session_id
        self.patient_id = patient_id
        self.workflow = workflow
        self.environment = environment
        self._run_metadata: dict = {}

    def on_llm_start(self, serialized: dict, prompts: list[str], **kwargs) -> None:
        self._run_metadata = {
            "session_id": self.session_id,
            "patient_id": self.patient_id or "anonymous",
            "workflow": self.workflow,
            "environment": self.environment,
            "prompt_count": len(prompts),
            "model": serialized.get("id", ["unknown"])[-1],
        }

    def on_llm_end(self, response: LLMResult, **kwargs) -> None:
        usage = response.llm_output or {}
        token_usage = usage.get("token_usage", {})
        self._run_metadata.update({
            "prompt_tokens": token_usage.get("prompt_tokens", 0),
            "completion_tokens": token_usage.get("completion_tokens", 0),
            "total_tokens": token_usage.get("total_tokens", 0),
        })

    def on_llm_error(self, error: Exception, **kwargs) -> None:
        self._run_metadata["error"] = str(error)
        self._run_metadata["error_type"] = type(error).__name__

    @property
    def last_run_metadata(self) -> dict:
        return self._run_metadata.copy()


def build_run_config(
    session_id: str,
    patient_id: str | None = None,
    workflow: str = "unknown",
    tags: list[str] | None = None,
) -> dict:
    """Build a LangChain/LangGraph run config with metadata and callbacks.

    Pass the returned dict as ``config=`` to any ``.invoke()`` call.
    """
    handler = MetadataCallbackHandler(
        session_id=session_id,
        patient_id=patient_id,
        workflow=workflow,
    )
    return {
        "configurable": {"thread_id": session_id},
        "callbacks": [handler],
        "tags": tags or [workflow],
        "metadata": {
            "session_id": session_id,
            "patient_id": patient_id or "anonymous",
            "workflow": workflow,
        },
    }
