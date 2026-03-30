"""Part 6 — Top-level multi-agent orchestration graph."""

from langchain_core.messages import AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from part_06_multi_agent.orchestrator.state import SupervisorState
from part_06_multi_agent.orchestrator.router import classify_intent
from part_06_multi_agent.agents.appointment_agent import run_appointment_agent
from part_06_multi_agent.agents.billing_agent import run_billing_agent
from part_06_multi_agent.agents.records_agent import run_records_agent
from part_06_multi_agent.agents.triage_agent import run_triage_agent
from part_06_multi_agent.agents.supervisor import run_supervisor
from shared.logger import logger


# ── Node functions ────────────────────────────────────────────────────────────

async def supervisor_node(state: SupervisorState) -> dict:
    """Classify intent and potentially handle general queries."""
    last_human = next(
        (m.content for m in reversed(state["messages"]) if m.type == "human"),
        ""
    )
    intent, confidence = await classify_intent(last_human)
    logger.info(f"Intent classified: {intent} (confidence={confidence:.2f})")

    response_content = None
    if intent == "general":
        response_content = await run_supervisor(last_human, intent)

    updates: dict = {"intent": intent}
    if response_content:
        updates["messages"] = [AIMessage(content=response_content)]
        updates["final_response"] = response_content
        updates["agent_used"] = "supervisor"

    return updates


async def appointment_node(state: SupervisorState) -> dict:
    last_human = next(
        (m.content for m in reversed(state["messages"]) if m.type == "human"), ""
    )
    response = await run_appointment_agent(last_human)
    return {
        "messages": [AIMessage(content=response)],
        "final_response": response,
        "agent_used": "appointment",
    }


async def billing_node(state: SupervisorState) -> dict:
    last_human = next(
        (m.content for m in reversed(state["messages"]) if m.type == "human"), ""
    )
    response = await run_billing_agent(last_human)
    return {
        "messages": [AIMessage(content=response)],
        "final_response": response,
        "agent_used": "billing",
    }


async def records_node(state: SupervisorState) -> dict:
    last_human = next(
        (m.content for m in reversed(state["messages"]) if m.type == "human"), ""
    )
    response = await run_records_agent(last_human)
    return {
        "messages": [AIMessage(content=response)],
        "final_response": response,
        "agent_used": "records",
    }


async def triage_node(state: SupervisorState) -> dict:
    last_human = next(
        (m.content for m in reversed(state["messages"]) if m.type == "human"), ""
    )
    response = await run_triage_agent(last_human)
    return {
        "messages": [AIMessage(content=response)],
        "final_response": response,
        "agent_used": "triage",
    }


# ── Routing ───────────────────────────────────────────────────────────────────

def route_intent(state: SupervisorState) -> str:
    intent = state.get("intent", "general")
    # If supervisor already handled it (general intent), go to END
    if state.get("final_response"):
        return END
    return intent


# ── Graph Assembly ────────────────────────────────────────────────────────────

def build_multi_agent_graph(checkpointer=None):
    graph = StateGraph(SupervisorState)

    graph.add_node("supervisor", supervisor_node)
    graph.add_node("appointment", appointment_node)
    graph.add_node("billing", billing_node)
    graph.add_node("records", records_node)
    graph.add_node("triage", triage_node)

    graph.add_edge(START, "supervisor")

    graph.add_conditional_edges(
        "supervisor",
        route_intent,
        {
            "appointment": "appointment",
            "billing": "billing",
            "records": "records",
            "triage": "triage",
            END: END,
        },
    )

    for node in ["appointment", "billing", "records", "triage"]:
        graph.add_edge(node, END)

    saver = checkpointer or MemorySaver()
    return graph.compile(checkpointer=saver)


multi_agent_graph = build_multi_agent_graph()
