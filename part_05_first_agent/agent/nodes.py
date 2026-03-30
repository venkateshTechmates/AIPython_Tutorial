"""Part 5 — All node functions for the triage agent graph."""

import json
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from part_05_first_agent.agent.state import TriageState
from shared.config import get_settings
from shared.logger import logger

settings = get_settings()


def _get_llm() -> ChatOpenAI:
    return ChatOpenAI(
        model=settings.llm_model,
        openai_api_key=settings.openai_api_key,
        temperature=0.3,
    )


def intake_node(state: TriageState) -> dict:
    """Collect patient name and primary complaint."""
    llm = _get_llm()

    system = SystemMessage(content=(
        "You are a hospital triage nurse. Your job is to collect the patient's name "
        "and their primary complaint. Ask one question at a time. Be warm and professional. "
        "If you have both the name and the main complaint, end your message with: "
        "INTAKE_COMPLETE: {name} | {complaint}"
    ))

    messages = [system] + state["messages"]
    response = llm.invoke(messages)

    # Check if intake is complete
    intake_complete = False
    patient_name = state.get("patient_name")
    symptoms = list(state.get("symptoms", []))

    if "INTAKE_COMPLETE:" in response.content:
        try:
            tag_start = response.content.index("INTAKE_COMPLETE:")
            tag_content = response.content[tag_start + len("INTAKE_COMPLETE:"):].strip()
            parts = tag_content.split("|")
            if len(parts) == 2:
                patient_name = parts[0].strip()
                complaint = parts[1].strip()
                symptoms = [complaint]
                intake_complete = True
                # Clean the response for display
                clean_content = response.content[:tag_start].strip()
                response = AIMessage(content=clean_content or f"Thank you, {patient_name}. I've noted your concern.")
        except Exception:
            pass

    return {
        "messages": [response],
        "intake_complete": intake_complete,
        "patient_name": patient_name,
        "symptoms": symptoms,
    }


def symptom_analysis_node(state: TriageState) -> dict:
    """Deep symptom analysis to extract urgency signals."""
    llm = _get_llm()

    symptoms_text = ", ".join(state.get("symptoms", []))

    system = SystemMessage(content=(
        "You are a clinical triage specialist. Analyze the patient's symptoms and ask "
        "targeted follow-up questions to determine: severity, duration, associated symptoms, "
        "and red flag signs. Ask no more than 3 follow-up questions. "
        "If you have enough information, end with: "
        "ANALYSIS_COMPLETE: {json with 'symptoms_detail' list and 'severity_indicators' list}"
    ))

    messages = [system, HumanMessage(content=f"Patient: {state.get('patient_name', 'Unknown')}\nReported: {symptoms_text}")] + state["messages"][-4:]
    response = llm.invoke(messages)

    analysis_complete = False
    symptoms = list(state.get("symptoms", []))

    if "ANALYSIS_COMPLETE:" in response.content:
        try:
            tag_start = response.content.index("ANALYSIS_COMPLETE:")
            json_str = response.content[tag_start + len("ANALYSIS_COMPLETE:"):].strip()
            data = json.loads(json_str)
            symptoms = data.get("symptoms_detail", symptoms)
            analysis_complete = True
            clean_content = response.content[:tag_start].strip()
            response = AIMessage(content=clean_content or "I've gathered enough information to assess your situation.")
        except Exception:
            analysis_complete = True  # Proceed even if parse fails

    return {
        "messages": [response],
        "symptoms": symptoms,
        "analysis_complete": analysis_complete,
    }


def urgency_classification_node(state: TriageState) -> dict:
    """Classify urgency level 1-5 based on symptoms."""
    llm = _get_llm()

    symptoms_text = "; ".join(state.get("symptoms", ["unspecified complaint"]))

    classification_prompt = f"""
Patient: {state.get("patient_name", "Unknown")}
Symptoms: {symptoms_text}

Classify the triage urgency level:
1 = IMMEDIATE (life-threatening, red — call 911)
2 = EMERGENT (serious, orange — see within 10 min)
3 = URGENT (significant, yellow — see within 30 min)
4 = SEMI-URGENT (non-acute, green — see within 1 hour)
5 = NON-URGENT (minor, blue — see within 2 hours)

Respond with ONLY valid JSON:
{{"urgency_level": <1-5>, "urgency_label": "<IMMEDIATE|EMERGENT|URGENT|SEMI-URGENT|NON-URGENT>", "reasoning": "<brief clinical reasoning>"}}
"""

    response = llm.invoke([HumanMessage(content=classification_prompt)])

    urgency_level = 4
    urgency_label = "SEMI-URGENT"

    try:
        data = json.loads(response.content.strip())
        urgency_level = int(data["urgency_level"])
        urgency_label = data["urgency_label"]
    except Exception as e:
        logger.warning(f"Failed to parse urgency classification: {e}")

    return {
        "urgency_level": urgency_level,
        "urgency_label": urgency_label,
    }


def recommendation_node(state: TriageState) -> dict:
    """Generate a patient-facing recommendation based on triage level."""
    llm = _get_llm()

    level = state.get("urgency_level", 4)
    label = state.get("urgency_label", "SEMI-URGENT")
    name = state.get("patient_name", "there")
    symptoms = "; ".join(state.get("symptoms", []))

    prompt = f"""
Patient: {name}
Urgency: Level {level} ({label})
Symptoms: {symptoms}

Provide a clear, compassionate recommendation for the patient. Include:
1. What they should do right now (call 911, go to ER, wait for nurse, etc.)
2. What to expect
3. Any immediate precautions they should take

Keep it to 3-4 sentences. Use plain language, not medical jargon.
"""
    response = llm.invoke([HumanMessage(content=prompt)])
    recommendation = response.content

    # High urgency — add emergency note
    if level <= 2:
        recommendation = (
            "⚠️ EMERGENCY: Please call 911 or go to the nearest Emergency Room immediately. "
            + recommendation
        )

    final_message = AIMessage(
        content=f"**Triage Assessment Complete**\n\n"
                f"**Urgency Level:** {level}/5 — {label}\n\n"
                f"**Recommendation:** {recommendation}"
    )

    return {
        "messages": [final_message],
        "recommendation": recommendation,
    }
