"""Part 14 — Capstone: Individual pipeline nodes for the patient journey graph."""

import json
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.language_models import BaseChatModel

from platform.state import PatientJourneyState


# ---------------------------------------------------------------------------
# Node 1 — Context injection
# ---------------------------------------------------------------------------

def inject_patient_context(state: PatientJourneyState) -> PatientJourneyState:
    """Pull long-term memory and prepend it as a system message."""
    if state.get("context_injected") or not state.get("patient_id"):
        return {"context_injected": True}

    # In a real deployment, MemoryManager lives in part_08
    patient_id = state["patient_id"]
    # Simplified context for capstone (avoiding cross-part imports that may fail)
    patient_context = f"[Patient Context: ID={patient_id} — preferences and history loaded from memory store]"

    system_msg = SystemMessage(content=(
        "You are the Hospital Intelligence Platform AI Assistant.\n\n"
        "You integrate scheduling, billing, medical records, triage, and clinical support.\n\n"
        f"{patient_context}\n\n"
        "Always be professional, empathetic, and safety-focused."
    ))

    messages = state.get("messages", [])
    if not messages or messages[0].type != "system":
        return {
            "messages": [system_msg] + list(messages),
            "patient_context": patient_context,
            "context_injected": True,
        }
    return {"context_injected": True}


# ---------------------------------------------------------------------------
# Node 2 — Intent classifier
# ---------------------------------------------------------------------------

def classify_intent(llm: BaseChatModel):
    """Return a node function that classifies user intent."""

    CLASSIFY_PROMPT = """Classify the following patient message into ONE of these categories:
appointment, billing, records, triage, general

Message: {message}

Respond with JSON only: {{"intent": "<category>", "confidence": <0.0-1.0>, "is_emergency": <true|false>}}"""

    def node(state: PatientJourneyState) -> PatientJourneyState:
        messages = state.get("messages", [])
        human_messages = [m for m in messages if m.type == "human"]
        if not human_messages:
            return {"intent": "general", "intent_confidence": 0.5, "is_emergency": False}

        last_message = human_messages[-1].content
        prompt = CLASSIFY_PROMPT.format(message=last_message)
        response = llm.invoke([HumanMessage(content=prompt)])

        try:
            parsed = json.loads(response.content)
            return {
                "intent": parsed.get("intent", "general"),
                "intent_confidence": float(parsed.get("confidence", 0.5)),
                "is_emergency": bool(parsed.get("is_emergency", False)),
            }
        except (json.JSONDecodeError, ValueError):
            return {"intent": "general", "intent_confidence": 0.0, "is_emergency": False}

    return node


# ---------------------------------------------------------------------------
# Node 3 — Emergency escalation
# ---------------------------------------------------------------------------

def emergency_escalation(state: PatientJourneyState) -> PatientJourneyState:
    """Immediate response for emergency situations — skip all other processing."""
    emergency_response = (
        "🚨 EMERGENCY ALERT 🚨\n\n"
        "Based on your description, this may be a medical emergency.\n\n"
        "IMMEDIATE ACTIONS:\n"
        "1. Call 911 immediately if in the US\n"
        "2. Go to the nearest Emergency Room\n"
        "3. Do NOT drive yourself\n"
        "4. Tell someone near you about your symptoms\n\n"
        "If you are at our facility, press the emergency call button or notify any staff member immediately."
    )
    return {
        "final_response": emergency_response,
        "urgency_level": 1,
        "urgency_label": "CRITICAL",
        "messages": [AIMessage(content=emergency_response)],
    }


# ---------------------------------------------------------------------------
# Node 4 — Tool calling node
# ---------------------------------------------------------------------------

def tool_calling_node(llm_with_tools):
    """Return a node that invokes the LLM with tools bound."""

    def node(state: PatientJourneyState) -> PatientJourneyState:
        messages = state.get("messages", [])
        response = llm_with_tools.invoke(messages)
        return {"messages": [response]}

    return node


# ---------------------------------------------------------------------------
# Node 5 — RAG retrieval node
# ---------------------------------------------------------------------------

def rag_retrieval(state: PatientJourneyState) -> PatientJourneyState:
    """Perform semantic search over hospital documents for context."""
    # In production this would call the Qdrant-backed retriever from Part 4
    # Here we return a placeholder for capstone wiring
    messages = state.get("messages", [])
    human_messages = [m for m in messages if m.type == "human"]
    if not human_messages:
        return {"rag_context": "", "rag_sources": []}

    query = human_messages[-1].content
    # Simulate retrieval
    rag_context = (
        f"[Retrieved context for: '{query[:60]}...' — "
        "Relevant hospital policies and clinical guidelines loaded]"
    )
    return {"rag_context": rag_context, "rag_sources": ["Hospital Policy DB"]}


# ---------------------------------------------------------------------------
# Node 6 — Final response synthesis
# ---------------------------------------------------------------------------

def synthesize_response(llm: BaseChatModel):
    """Return a node that synthesizes the final patient-facing response."""

    def node(state: PatientJourneyState) -> PatientJourneyState:
        if state.get("final_response"):
            return {}  # Already set (e.g., emergency escalation)

        messages = state.get("messages", [])
        rag_ctx = state.get("rag_context", "")
        tool_results = state.get("tool_results", [])

        synthesis_prompt = []
        if rag_ctx:
            synthesis_prompt.append(f"Relevant context:\n{rag_ctx}")
        if tool_results:
            synthesis_prompt.append(f"Tool results:\n{json.dumps(tool_results[:3], indent=2)}")

        if synthesis_prompt:
            messages = list(messages) + [
                HumanMessage(content="\n\n".join(synthesis_prompt) + "\n\nPlease provide a helpful response.")
            ]

        response = llm.invoke(messages)
        return {
            "final_response": response.content,
            "messages": [response],
        }

    return node
