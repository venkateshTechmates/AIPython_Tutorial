"""Part 9 — Prescription approval workflow with human interrupt."""

from typing import Annotated
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.language_models import BaseChatModel
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt, Command
from typing_extensions import TypedDict


class PrescriptionState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    patient_id: str
    drug_name: str
    dosage: str
    prescriber: str
    ai_recommendation: str
    human_decision: str  # "approved" | "rejected" | "pending"
    rejection_reason: str
    workflow_complete: bool


PRESCRIPTION_REVIEW_PROMPT = """You are a clinical pharmacist AI assistant reviewing a prescription.

Patient ID: {patient_id}
Drug: {drug_name}
Dosage: {dosage}
Prescriber: {prescriber}

Analyze this prescription and provide:
1. Clinical appropriateness assessment
2. Potential drug interactions (common ones)
3. Dosage range check (is this within normal range?)
4. Your recommendation: APPROVE or FLAG_FOR_REVIEW

Format your response as a clinical review note."""


def build_prescription_workflow(llm: BaseChatModel, checkpointer=None):
    """Build a prescription approval workflow with human-in-the-loop interrupt."""

    def analyze_prescription(state: PrescriptionState) -> PrescriptionState:
        """AI analyzes the prescription and generates a recommendation."""
        prompt = PRESCRIPTION_REVIEW_PROMPT.format(
            patient_id=state["patient_id"],
            drug_name=state["drug_name"],
            dosage=state["dosage"],
            prescriber=state["prescriber"],
        )
        response = llm.invoke([HumanMessage(content=prompt)])
        return {
            "ai_recommendation": response.content,
            "messages": [AIMessage(content=f"AI Review Complete:\n\n{response.content}")],
        }

    def human_review(state: PrescriptionState) -> Command:
        """Interrupt for human pharmacist decision."""
        # Present review summary to the human
        review_summary = (
            f"PRESCRIPTION PENDING REVIEW\n"
            f"{'=' * 40}\n"
            f"Patient: {state['patient_id']}\n"
            f"Drug: {state['drug_name']} — {state['dosage']}\n"
            f"Prescriber: {state['prescriber']}\n\n"
            f"AI Analysis:\n{state['ai_recommendation']}\n\n"
            f"Please approve or reject this prescription."
        )

        # interrupt() pauses execution and surfaces the value to the runner
        decision = interrupt({"review_summary": review_summary, "action_required": "approve_or_reject"})

        # When resumed, decision contains {"decision": "approved"|"rejected", "reason": "..."}
        human_dec = decision.get("decision", "rejected")
        reason = decision.get("reason", "")
        return Command(
            goto="finalize" if human_dec == "approved" else "reject_prescription",
            update={"human_decision": human_dec, "rejection_reason": reason},
        )

    def finalize(state: PrescriptionState) -> PrescriptionState:
        """Prescription approved — generate dispensing instructions."""
        response = llm.invoke([
            HumanMessage(content=(
                f"The prescription for {state['drug_name']} {state['dosage']} has been approved "
                f"for patient {state['patient_id']}. Generate brief patient dispensing instructions."
            ))
        ])
        return {
            "messages": [AIMessage(content=f"APPROVED — Dispensing Instructions:\n{response.content}")],
            "workflow_complete": True,
        }

    def reject_prescription(state: PrescriptionState) -> PrescriptionState:
        """Handle rejection — notify with reason."""
        reason = state.get("rejection_reason") or "Does not meet clinical criteria."
        msg = (
            f"PRESCRIPTION REJECTED\n"
            f"Drug: {state['drug_name']} {state['dosage']}\n"
            f"Reason: {reason}\n"
            f"Please contact the prescriber to discuss alternatives."
        )
        return {
            "messages": [AIMessage(content=msg)],
            "workflow_complete": True,
        }

    graph = StateGraph(PrescriptionState)
    graph.add_node("analyze", analyze_prescription)
    graph.add_node("human_review", human_review)
    graph.add_node("finalize", finalize)
    graph.add_node("reject_prescription", reject_prescription)

    graph.add_edge(START, "analyze")
    graph.add_edge("analyze", "human_review")
    # human_review uses Command.goto — no explicit edges needed from it
    graph.add_edge("finalize", END)
    graph.add_edge("reject_prescription", END)

    return graph.compile(checkpointer=checkpointer or MemorySaver(), interrupt_before=["human_review"])
