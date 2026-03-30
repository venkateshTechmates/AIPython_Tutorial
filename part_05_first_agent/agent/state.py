"""Part 5 — Triage agent state definition."""

from typing import Annotated
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class TriageState(TypedDict):
    # Conversation messages (auto-merged by add_messages reducer)
    messages: Annotated[list[BaseMessage], add_messages]
    # Extracted symptom information
    symptoms: list[str]
    # Triage urgency output (1=immediate to 5=non-urgent)
    urgency_level: int | None
    # Human-readable urgency label
    urgency_label: str | None
    # Clinical recommendation text
    recommendation: str | None
    # Has intake been collected?
    intake_complete: bool
    # Symptom analysis completed?
    analysis_complete: bool
    # Patient's name (collected during intake)
    patient_name: str | None
