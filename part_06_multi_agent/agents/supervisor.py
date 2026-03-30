"""Part 6 — Supervisor agent with intent classification."""

import json
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from shared.config import get_settings

settings = get_settings()

SYSTEM_PROMPT = """\
You are the Hospital AI Supervisor. Your job is to:
1. Understand the patient's intent
2. Route to the appropriate specialist agent
3. Handle greetings and general hospital information yourself

Routing rules:
- appointment → Appointment Scheduling Agent
- billing → Billing & Insurance Agent  
- records → Medical Records Agent
- triage → Emergency Triage Agent
- general → Handle yourself with helpful hospital info

Always be welcoming and professional.
"""


async def run_supervisor(user_message: str, intent: str) -> str:
    """Supervisor handles general queries directly."""
    if intent != "general":
        return ""

    llm = ChatOpenAI(
        model=settings.llm_model,
        openai_api_key=settings.openai_api_key,
        temperature=0.5,
    )
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_message),
    ]
    response = await llm.ainvoke(messages)
    return response.content
