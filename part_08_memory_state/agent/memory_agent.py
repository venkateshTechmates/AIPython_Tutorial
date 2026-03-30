"""Part 8 — Memory-enabled LangGraph agent with context injection."""

from typing import Annotated
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_core.language_models import BaseChatModel
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from typing_extensions import TypedDict

from memory.manager import MemoryManager


class MemoryAgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    patient_id: str
    session_id: str
    context_injected: bool


SYSTEM_BASE = """You are a Hospital AI Assistant with persistent memory.

You have access to:
1. Patient's long-term preferences and clinical history
2. Recent conversation history from this session
3. Semantically similar past interactions

Use this context to provide personalized, continuous care.

IMPORTANT:
- Reference patient context naturally — don't mechanically repeat it
- If a patient mentions something new you should remember, mention that you've noted it
- For clinical facts (allergies, chronic conditions), always acknowledge and record mentally
- Never fabricate clinical history not present in the context
"""


def build_memory_agent_graph(llm: BaseChatModel, checkpointer=None):
    """Build a LangGraph with memory context injection at every turn."""

    def inject_context_node(state: MemoryAgentState) -> MemoryAgentState:
        """Prepend a context-rich system message before the LLM call."""
        if state.get("context_injected"):
            return state

        mgr = MemoryManager(
            patient_id=state["patient_id"],
            session_id=state["session_id"],
        )
        context_block = mgr.build_context_prompt()
        system_content = SYSTEM_BASE + "\n\n" + context_block
        system_msg = SystemMessage(content=system_content)

        existing = state["messages"]
        # Insert system message at position 0 if not already there
        if not existing or existing[0].type != "system":
            return {"messages": [system_msg] + list(existing), "context_injected": True}
        return {"context_injected": True}

    def llm_node(state: MemoryAgentState) -> MemoryAgentState:
        """Invoke the LLM and persist the exchange to memory."""
        response = llm.invoke(state["messages"])

        # Persist to short-term memory
        mgr = MemoryManager(
            patient_id=state["patient_id"],
            session_id=state["session_id"],
        )
        # Find the last human message
        for msg in reversed(state["messages"]):
            if isinstance(msg, HumanMessage):
                mgr.remember_user_message(msg.content)
                break
        mgr.remember_ai_response(response.content)

        return {"messages": [response]}

    graph = StateGraph(MemoryAgentState)
    graph.add_node("inject_context", inject_context_node)
    graph.add_node("llm", llm_node)

    graph.add_edge(START, "inject_context")
    graph.add_edge("inject_context", "llm")
    graph.add_edge("llm", END)

    return graph.compile(checkpointer=checkpointer or MemorySaver())
