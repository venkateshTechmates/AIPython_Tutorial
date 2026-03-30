"""Part 14 — Capstone: Unified platform state combining all prior parts."""

from typing import Annotated, Optional
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


class PatientJourneyState(TypedDict):
    """Full patient journey state — the master state object for the capstone platform."""

    # ── Conversation ─────────────────────────────────────────────────────────
    messages: Annotated[list[BaseMessage], add_messages]
    session_id: str
    patient_id: Optional[str]

    # ── Intent routing ────────────────────────────────────────────────────────
    intent: Optional[str]           # appointment | billing | records | triage | general
    intent_confidence: float

    # ── Tool call outputs ─────────────────────────────────────────────────────
    tool_results: list[dict]

    # ── RAG context ───────────────────────────────────────────────────────────
    rag_context: str
    rag_sources: list[str]

    # ── Triage ────────────────────────────────────────────────────────────────
    urgency_level: Optional[int]
    urgency_label: str

    # ── Workflow state ────────────────────────────────────────────────────────
    active_workflow: Optional[str]  # None | "prescription" | "billing" | "discharge"
    workflow_thread_id: Optional[str]
    awaiting_approval: bool

    # ── Memory ────────────────────────────────────────────────────────────────
    patient_context: str            # injected from MemoryManager.build_context_prompt()
    context_injected: bool

    # ── Response ──────────────────────────────────────────────────────────────
    final_response: str
    is_emergency: bool
    error: Optional[str]
