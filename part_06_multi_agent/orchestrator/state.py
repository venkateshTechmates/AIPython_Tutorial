"""Part 6 — Shared state schema for multi-agent orchestration."""

from typing import Annotated
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class SupervisorState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    # Detected intent from user query
    intent: str | None
    # Which sub-agent handled the request
    agent_used: str | None
    # Final response from sub-agent
    final_response: str | None
    # Error info if something went wrong
    error: str | None
