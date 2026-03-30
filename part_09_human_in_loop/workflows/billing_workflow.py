"""Part 9 — Billing authorization workflow with human-in-the-loop."""

from typing import Annotated
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.language_models import BaseChatModel
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt, Command
from typing_extensions import TypedDict


class BillingState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    patient_id: str
    invoice_id: str
    total_amount: float
    insurance_plan: str
    procedures: list[str]
    ai_assessment: str
    authorization_status: str  # "authorized" | "denied" | "pending"
    override_reason: str
    workflow_complete: bool


# Threshold above which human review is required
HIGH_VALUE_THRESHOLD = 5000.0


def build_billing_workflow(llm: BaseChatModel, checkpointer=None):
    """Build a billing authorization workflow with conditional human review."""

    def assess_claim(state: BillingState) -> Annotated[dict, None]:
        """AI assesses the billing claim for insurance authorization."""
        procedures_str = ", ".join(state.get("procedures") or ["General services"])
        prompt = (
            f"You are a medical billing AI reviewing an insurance authorization request.\n\n"
            f"Patient: {state['patient_id']} | Invoice: {state['invoice_id']}\n"
            f"Total: ${state['total_amount']:,.2f} | Plan: {state['insurance_plan']}\n"
            f"Procedures: {procedures_str}\n\n"
            f"Assess whether these procedures are typically covered, identify any potential "
            f"issues (e.g., prior auth required, experimental treatments), and give an "
            f"authorization recommendation: AUTO_APPROVE, NEEDS_REVIEW, or AUTO_DENY."
        )
        response = llm.invoke([HumanMessage(content=prompt)])
        return {
            "ai_assessment": response.content,
            "messages": [AIMessage(content=f"Billing Assessment:\n{response.content}")],
        }

    def route_by_assessment(state: BillingState) -> str:
        """Route to human review if high-value or AI flagged NEEDS_REVIEW."""
        content = state.get("ai_assessment", "")
        high_value = state["total_amount"] >= HIGH_VALUE_THRESHOLD
        needs_review = "NEEDS_REVIEW" in content
        auto_deny = "AUTO_DENY" in content

        if auto_deny:
            return "auto_deny"
        if high_value or needs_review:
            return "human_review"
        return "auto_approve"

    def auto_approve(state: BillingState) -> BillingState:
        return {
            "authorization_status": "authorized",
            "messages": [AIMessage(content=f"Invoice {state['invoice_id']} AUTO-APPROVED by AI.")],
            "workflow_complete": True,
        }

    def auto_deny(state: BillingState) -> BillingState:
        return {
            "authorization_status": "denied",
            "messages": [AIMessage(content=f"Invoice {state['invoice_id']} AUTO-DENIED. See AI assessment.")],
            "workflow_complete": True,
        }

    def human_review(state: BillingState) -> Command:
        """Interrupt for billing specialist review."""
        summary = (
            f"BILLING AUTHORIZATION REQUIRED\n{'=' * 40}\n"
            f"Patient: {state['patient_id']} | Invoice: {state['invoice_id']}\n"
            f"Amount: ${state['total_amount']:,.2f} | Plan: {state['insurance_plan']}\n\n"
            f"AI Assessment:\n{state['ai_assessment']}\n\n"
            f"Action required: authorize or deny."
        )
        decision = interrupt({"summary": summary, "action": "billing_authorization"})
        status = "authorized" if decision.get("authorized") else "denied"
        return Command(
            goto="complete_review",
            update={
                "authorization_status": status,
                "override_reason": decision.get("reason", ""),
            },
        )

    def complete_review(state: BillingState) -> BillingState:
        status = state["authorization_status"]
        msg = (
            f"Invoice {state['invoice_id']} {status.upper()} by billing specialist.\n"
            + (f"Reason: {state['override_reason']}" if state.get("override_reason") else "")
        )
        return {
            "messages": [AIMessage(content=msg)],
            "workflow_complete": True,
        }

    graph = StateGraph(BillingState)
    graph.add_node("assess_claim", assess_claim)
    graph.add_node("auto_approve", auto_approve)
    graph.add_node("auto_deny", auto_deny)
    graph.add_node("human_review", human_review)
    graph.add_node("complete_review", complete_review)

    graph.add_edge(START, "assess_claim")
    graph.add_conditional_edges("assess_claim", route_by_assessment)
    graph.add_edge("auto_approve", END)
    graph.add_edge("auto_deny", END)
    graph.add_edge("complete_review", END)

    return graph.compile(checkpointer=checkpointer or MemorySaver(), interrupt_before=["human_review"])
