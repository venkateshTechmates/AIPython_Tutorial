"""Part 7 — ReAct agent builder using LangChain tool-calling."""

from langchain_core.messages import SystemMessage
from langchain_core.language_models import BaseChatModel

from tools import ALL_TOOLS


SYSTEM_PROMPT = """You are a Hospital AI Assistant with access to real-time hospital tools.

You help patients, staff, and administrators with:
- Looking up patient records
- Scheduling and checking appointments  
- Retrieving and calculating billing information
- Looking up drug interactions, ICD-10 codes, and drug information
- General date/time calculations

INSTRUCTIONS:
1. Always use the available tools to fetch accurate, up-to-date information.
2. Do NOT make up patient data, invoice numbers, or medical information.
3. When asked about drug interactions, ALWAYS use the search_drug_interactions tool.
4. When scheduling appointments, confirm all details with the patient before proceeding.
5. For billing questions, retrieve the actual invoice using get_invoice_by_id when possible.
6. Be concise, professional, and patient-centered in your responses.
7. If a tool returns an error, explain it clearly and suggest alternatives."""


def build_react_agent(llm: BaseChatModel):
    """Bind tools to the LLM and return the tool-aware model.
    
    The returned model can be used inside a LangGraph node. It will emit
    AIMessage objects with ``tool_calls`` when it wants to invoke a tool.
    """
    return llm.bind_tools(ALL_TOOLS)


def get_system_message() -> SystemMessage:
    """Return the system message for the hospital assistant."""
    return SystemMessage(content=SYSTEM_PROMPT)
