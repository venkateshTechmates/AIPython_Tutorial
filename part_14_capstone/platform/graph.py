"""Part 14 — Capstone: Full patient journey LangGraph."""

from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.language_models import BaseChatModel

from platform.state import PatientJourneyState
from platform.nodes import (
    inject_patient_context,
    classify_intent,
    emergency_escalation,
    tool_calling_node,
    rag_retrieval,
    synthesize_response,
)

# Capstone imports all tools from Part 7
import sys
sys.path.append("../part_07_tool_calling")

try:
    from tools import ALL_TOOLS as HOSPITAL_TOOLS
except ImportError:
    HOSPITAL_TOOLS = []


def route_after_classification(state: PatientJourneyState) -> str:
    """Route based on intent and emergency flag."""
    if state.get("is_emergency"):
        return "emergency"
    intent = state.get("intent", "general")
    if intent in ("appointment", "billing", "records"):
        return "tools"
    if intent == "triage":
        return "rag"
    return "rag"  # general — use RAG for knowledge retrieval


def build_capstone_graph(llm: BaseChatModel, checkpointer=None) -> any:
    """Build the full Hospital Intelligence Platform graph.

    Flow:
        START
          → inject_context
          → classify_intent
          → [emergency | tools | rag]
          → synthesize
          → END
    """
    llm_with_tools = llm.bind_tools(HOSPITAL_TOOLS) if HOSPITAL_TOOLS else llm

    graph = StateGraph(PatientJourneyState)

    # Register nodes
    graph.add_node("inject_context", inject_patient_context)
    graph.add_node("classify", classify_intent(llm))
    graph.add_node("emergency", emergency_escalation)
    graph.add_node("llm_tools", tool_calling_node(llm_with_tools))
    graph.add_node("tool_executor", ToolNode(tools=HOSPITAL_TOOLS) if HOSPITAL_TOOLS else lambda s: s)
    graph.add_node("rag", rag_retrieval)
    graph.add_node("synthesize", synthesize_response(llm))

    # Edges
    graph.add_edge(START, "inject_context")
    graph.add_edge("inject_context", "classify")
    graph.add_conditional_edges("classify", route_after_classification, {
        "emergency": "emergency",
        "tools": "llm_tools",
        "rag": "rag",
    })
    graph.add_edge("emergency", END)

    # Tools loop (Part 7 pattern)
    if HOSPITAL_TOOLS:
        graph.add_conditional_edges("llm_tools", tools_condition, {
            "tools": "tool_executor",
            END: "synthesize",
        })
        graph.add_edge("tool_executor", "llm_tools")
    else:
        graph.add_edge("llm_tools", "synthesize")

    graph.add_edge("rag", "synthesize")
    graph.add_edge("synthesize", END)

    return graph.compile(checkpointer=checkpointer or MemorySaver())
