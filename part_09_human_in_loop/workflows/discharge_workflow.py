"""Part 9 — Patient discharge workflow with multi-step human approvals."""

from typing import Annotated
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.language_models import BaseChatModel
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt, Command
from typing_extensions import TypedDict


class DischargeState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    patient_id: str
    admitting_diagnosis: str
    discharge_diagnosis: str
    length_of_stay_days: int
    discharge_medications: list[str]
    follow_up_required: bool
    discharge_summary: str           # AI-generated
    physician_signed: bool
    nurse_reviewed: bool
    pharmacy_cleared: bool
    discharge_ready: bool
    workflow_complete: bool


def build_discharge_workflow(llm: BaseChatModel, checkpointer=None):
    """Build a discharge workflow requiring physician, nurse, and pharmacy sign-offs."""

    def generate_discharge_summary(state: DischargeState) -> DischargeState:
        meds = ", ".join(state.get("discharge_medications") or ["None"])
        prompt = (
            f"Generate a concise hospital discharge summary for:\n"
            f"Patient: {state['patient_id']}\n"
            f"Admission diagnosis: {state['admitting_diagnosis']}\n"
            f"Discharge diagnosis: {state['discharge_diagnosis']}\n"
            f"Length of stay: {state['length_of_stay_days']} days\n"
            f"Discharge medications: {meds}\n"
            f"Follow-up required: {state['follow_up_required']}\n\n"
            f"Include: condition on discharge, activity restrictions, medication instructions, "
            f"when to seek emergency care, and follow-up appointments."
        )
        response = llm.invoke([HumanMessage(content=prompt)])
        return {
            "discharge_summary": response.content,
            "messages": [AIMessage(content=f"Draft Discharge Summary:\n\n{response.content}")],
        }

    def physician_signoff(state: DischargeState) -> Command:
        """Interrupt for physician review and signature."""
        decision = interrupt({
            "summary": state["discharge_summary"],
            "action": "physician_signature",
            "patient_id": state["patient_id"],
        })
        signed = decision.get("signed", False)
        amendments = decision.get("amendments", "")
        if amendments:
            amended_summary = state["discharge_summary"] + f"\n\n[Physician Amendment]: {amendments}"
        else:
            amended_summary = state["discharge_summary"]
        return Command(
            goto="nurse_review",
            update={"physician_signed": signed, "discharge_summary": amended_summary},
        )

    def nurse_review(state: DischargeState) -> Command:
        """Interrupt for nursing review — patient education and readiness check."""
        decision = interrupt({
            "action": "nurse_patient_education_review",
            "patient_id": state["patient_id"],
            "medications": state.get("discharge_medications"),
            "follow_up": state["follow_up_required"],
        })
        reviewed = decision.get("reviewed", False)
        return Command(goto="pharmacy_check", update={"nurse_reviewed": reviewed})

    def pharmacy_check(state: DischargeState) -> Command:
        """Interrupt for pharmacy medication reconciliation."""
        decision = interrupt({
            "action": "pharmacy_medication_reconciliation",
            "patient_id": state["patient_id"],
            "medications": state.get("discharge_medications"),
        })
        cleared = decision.get("cleared", False)
        return Command(goto="finalize_discharge", update={"pharmacy_cleared": cleared})

    def finalize_discharge(state: DischargeState) -> DischargeState:
        all_approved = (
            state.get("physician_signed")
            and state.get("nurse_reviewed")
            and state.get("pharmacy_cleared")
        )

        if all_approved:
            msg = (
                f"DISCHARGE AUTHORIZED — Patient {state['patient_id']}\n"
                f"All sign-offs complete: Physician ✓ | Nurse ✓ | Pharmacy ✓\n\n"
                f"Final Discharge Summary:\n{state['discharge_summary']}"
            )
        else:
            pending = [
                name for name, flag in [
                    ("Physician", state.get("physician_signed")),
                    ("Nurse", state.get("nurse_reviewed")),
                    ("Pharmacy", state.get("pharmacy_cleared")),
                ]
                if not flag
            ]
            msg = f"DISCHARGE BLOCKED — Pending approvals: {', '.join(pending)}"

        return {
            "discharge_ready": all_approved,
            "messages": [AIMessage(content=msg)],
            "workflow_complete": True,
        }

    graph = StateGraph(DischargeState)
    graph.add_node("generate_summary", generate_discharge_summary)
    graph.add_node("physician_signoff", physician_signoff)
    graph.add_node("nurse_review", nurse_review)
    graph.add_node("pharmacy_check", pharmacy_check)
    graph.add_node("finalize_discharge", finalize_discharge)

    graph.add_edge(START, "generate_summary")
    graph.add_edge("generate_summary", "physician_signoff")
    graph.add_edge("finalize_discharge", END)

    return graph.compile(
        checkpointer=checkpointer or MemorySaver(),
        interrupt_before=["physician_signoff", "nurse_review", "pharmacy_check"],
    )
