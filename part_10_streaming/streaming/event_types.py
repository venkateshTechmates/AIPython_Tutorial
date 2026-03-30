"""Part 10 — SSE event type definitions for streaming agent responses."""

from enum import Enum
from typing import Any
from pydantic import BaseModel


class StreamEventType(str, Enum):
    STREAM_START = "stream_start"
    TOKEN = "token"
    TOOL_START = "tool_start"
    TOOL_END = "tool_end"
    NODE_START = "node_start"
    NODE_END = "node_end"
    STREAM_END = "stream_end"
    ERROR = "error"


class StreamEvent(BaseModel):
    event: StreamEventType
    data: Any
    run_id: str | None = None
    metadata: dict | None = None

    def to_sse(self) -> str:
        """Format as Server-Sent Events wire format."""
        import json
        payload = json.dumps(self.model_dump())
        return f"data: {payload}\n\n"
