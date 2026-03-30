"""Part 6 — Triage sub-agent (simplified version for multi-agent use)."""

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from shared.config import get_settings

settings = get_settings()

SYSTEM_PROMPT = """\
You are a Hospital Triage Assessment Agent.
Your role is to:
1. Assess the severity of patient symptoms
2. Provide urgency level (1=Emergency, 2=Urgent, 3=Semi-urgent, 4=Routine, 5=Non-urgent)
3. Give clear recommendations (call 911, go to ER, schedule appointment, etc.)
4. Ask clarifying questions about symptoms when needed

Always err on the side of caution. For ANY chest pain, difficulty breathing, or severe symptoms,
immediately recommend emergency services.
"""


async def run_triage_agent(user_message: str, conversation_history: list = None) -> str:
    llm = ChatOpenAI(
        model=settings.llm_model,
        openai_api_key=settings.openai_api_key,
        temperature=0.1,
    )
    messages = [SystemMessage(content=SYSTEM_PROMPT)]
    if conversation_history:
        messages.extend(conversation_history)
    messages.append(HumanMessage(content=user_message))

    response = await llm.ainvoke(messages)
    return response.content
