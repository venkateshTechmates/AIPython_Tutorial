"""Part 6 — Billing sub-agent."""

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from shared.config import get_settings

settings = get_settings()

SYSTEM_PROMPT = """\
You are the Hospital Billing and Insurance Agent.
You help patients with:
- Understanding their bills and charges
- Insurance coverage questions and pre-authorization
- Payment plan options and financial assistance
- Disputing charges or requesting itemized statements
- Understanding CPT codes and what services were billed

Be transparent, empathetic, and explain financial information clearly.
For complex billing disputes, offer to escalate to the billing department.
"""


async def run_billing_agent(user_message: str, conversation_history: list = None) -> str:
    llm = ChatOpenAI(
        model=settings.llm_model,
        openai_api_key=settings.openai_api_key,
        temperature=0.3,
    )
    messages = [SystemMessage(content=SYSTEM_PROMPT)]
    if conversation_history:
        messages.extend(conversation_history)
    messages.append(HumanMessage(content=user_message))

    response = await llm.ainvoke(messages)
    return response.content
