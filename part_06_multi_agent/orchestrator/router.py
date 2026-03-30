"""Part 6 — Intent classification & routing logic."""

import json
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from shared.config import get_settings

settings = get_settings()

INTENTS = {
    "appointment": "Scheduling, cancelling, or checking appointments; doctor availability",
    "billing": "Invoices, insurance, payments, charges, cost estimates",
    "records": "Medical records, test results, diagnoses, prescriptions history",
    "triage": "Symptoms, medical concerns, pain, illness, urgent care needs",
    "general": "General hospital information, directions, policies, other",
}

ROUTING_PROMPT = f"""You are a hospital query router. Classify the user's intent into one category:
{chr(10).join(f'- {k}: {v}' for k, v in INTENTS.items())}

Respond ONLY with valid JSON: {{"intent": "<category>", "confidence": 0.0-1.0}}
"""


async def classify_intent(user_message: str) -> tuple[str, float]:
    """Return (intent, confidence) for a given user message."""
    llm = ChatOpenAI(
        model=settings.llm_model,
        openai_api_key=settings.openai_api_key,
        temperature=0.0,
    )
    response = await llm.ainvoke([
        HumanMessage(content=ROUTING_PROMPT + f"\n\nUser query: {user_message}")
    ])
    try:
        data = json.loads(response.content.strip())
        return data["intent"], float(data["confidence"])
    except Exception:
        return "general", 0.0
