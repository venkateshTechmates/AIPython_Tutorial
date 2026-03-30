"""Part 6 — Medical Records sub-agent."""

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from shared.config import get_settings

settings = get_settings()

SYSTEM_PROMPT = """\
You are the Hospital Medical Records Agent.
You help patients and clinical staff with:
- Accessing visit summaries and medical history
- Understanding diagnoses and ICD codes
- Retrieving lab results and imaging reports
- Understanding prescribed medications and dosages
- Requesting medical record transfers

Always emphasize patient privacy. Verify patient identity before discussing records.
Remind patients that full records require formal request through the medical records office.
"""


async def run_records_agent(user_message: str, conversation_history: list = None) -> str:
    llm = ChatOpenAI(
        model=settings.llm_model,
        openai_api_key=settings.openai_api_key,
        temperature=0.2,
    )
    messages = [SystemMessage(content=SYSTEM_PROMPT)]
    if conversation_history:
        messages.extend(conversation_history)
    messages.append(HumanMessage(content=user_message))

    response = await llm.ainvoke(messages)
    return response.content
