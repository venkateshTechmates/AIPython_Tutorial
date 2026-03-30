"""Part 5 — Triage agent graph assembly."""

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from part_05_first_agent.agent.state import TriageState
from part_05_first_agent.agent.nodes import (
    intake_node,
    symptom_analysis_node,
    urgency_classification_node,
    recommendation_node,
)
from part_05_first_agent.agent.edges import (
    should_continue_intake,
    should_continue_analysis,
    route_by_urgency,
)


def build_triage_graph(checkpointer=None):
    """
    Build and compile the triage agent state graph.

    Graph flow:
    START → intake → (loop) → analyze → (loop) → classify → recommend → END
    """
    graph = StateGraph(TriageState)

    # Add nodes
    graph.add_node("intake", intake_node)
    graph.add_node("analyze", symptom_analysis_node)
    graph.add_node("classify", urgency_classification_node)
    graph.add_node("recommend", recommendation_node)

    # Entry point
    graph.add_edge(START, "intake")

    # Intake loop
    graph.add_conditional_edges(
        "intake",
        should_continue_intake,
        {"intake": "intake", "analyze": "analyze"},
    )

    # Analysis loop
    graph.add_conditional_edges(
        "analyze",
        should_continue_analysis,
        {"analyze": "analyze", "classify": "classify"},
    )

    # After classification, always recommend
    graph.add_conditional_edges(
        "classify",
        route_by_urgency,
        {"recommend": "recommend"},
    )

    # End
    graph.add_edge("recommend", END)

    # Use in-memory checkpointer by default (swap for SqliteSaver in production)
    saver = checkpointer or MemorySaver()
    return graph.compile(checkpointer=saver)


# Default compiled graph instance
triage_graph = build_triage_graph()


def get_graph_mermaid() -> str:
    """Return Mermaid diagram representation of the graph."""
    return triage_graph.get_graph().draw_mermaid()
