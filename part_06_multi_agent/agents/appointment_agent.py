"""Part 6 — Appointment sub-agent."""

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from shared.config import get_settings

settings = get_settings()

SYSTEM_PROMPT = """\
You are the Hospital Appointment Scheduling Agent.
You help patients:
- Schedule new appointments with available doctors
- Check, modify, or cancel existing appointments
- Get information about doctor availability and specialties
- Understand wait times and appointment types

Be helpful, efficient, and confirm all appointment details clearly.
Always ask for patient name and preferred date/time when scheduling new appointments.
"""


async def run_appointment_agent(user_message: str, conversation_history: list = None) -> str:
    llm = ChatOpenAI(
        model=settings.llm_model,
        openai_api_key=settings.openai_api_key,
        temperature=0.4,
    )
    messages = [SystemMessage(content=SYSTEM_PROMPT)]
    if conversation_history:
        messages.extend(conversation_history)
    messages.append(HumanMessage(content=user_message))

    response = await llm.ainvoke(messages)
    return response.content
