"""Part 10 — Streaming LangGraph agent (minimal, no tools — pure token streaming)."""

from typing import Annotated
from langchain_core.messages import BaseMessage, SystemMessage
from langchain_core.language_models import BaseChatModel
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from typing_extensions import TypedDict


SYSTEM_PROMPT = """You are a Hospital AI Assistant. You provide helpful, accurate information 
about healthcare, appointments, billing, and medical questions.

Be concise, clear, and always recommend consulting a physician for medical decisions.
Never diagnose — only provide general information."""


class StreamingAgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def build_streaming_agent(llm: BaseChatModel, checkpointer=None):
    """Build a simple streaming-capable LangGraph agent.

    This agent does not use tools so token-level streaming works transparently.
    For tool+streaming, see the combined version in Part 14 (capstone).
    """

    def chat_node(state: StreamingAgentState) -> StreamingAgentState:
        messages = state["messages"]
        if not messages or messages[0].type != "system":
            messages = [SystemMessage(content=SYSTEM_PROMPT)] + list(messages)
        response = llm.invoke(messages)
        return {"messages": [response]}

    graph = StateGraph(StreamingAgentState)
    graph.add_node("chat", chat_node)
    graph.add_edge(START, "chat")
    graph.add_edge("chat", END)

    return graph.compile(checkpointer=checkpointer or MemorySaver())
