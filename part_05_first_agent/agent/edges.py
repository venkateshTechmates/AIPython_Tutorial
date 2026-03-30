"""Part 5 — Conditional edge logic for triage agent."""

from part_05_first_agent.agent.state import TriageState


def should_continue_intake(state: TriageState) -> str:
    """Continue intake until patient provides name + complaint."""
    if state.get("intake_complete"):
        return "analyze"
    return "intake"


def should_continue_analysis(state: TriageState) -> str:
    """Continue analysis until we have enough symptom data."""
    if state.get("analysis_complete"):
        return "classify"
    return "analyze"


def route_by_urgency(state: TriageState) -> str:
    """Route to recommendation node — can branch here for urgent escalation."""
    level = state.get("urgency_level", 4)
    # All paths lead to recommendation; differentiation is in the content
    return "recommend"
