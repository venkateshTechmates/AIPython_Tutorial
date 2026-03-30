import type { PartData } from "../../types";

export const part07: PartData = {
  id: "07",
  title: "Tool Calling",
  goal: "Equip the hospital agent with 13 real tools: patient lookup, appointment scheduling, billing, and drug interactions.",
  phase: 3,
  phaseLabel: "Multi-Agent Systems",
  folder: "part_07_tool_calling",
  estimatedHours: 5,
  difficulty: "intermediate",
  prerequisites: ["05", "06"],
  unlocks: ["08"],
  whatYouBuild: [
    { label: "POST /agent/chat", description: "Chat with tool-enabled ReAct agent" },
    { label: "GET /tools", description: "List all 13 available tools with schemas" },
  ],
  mermaidDiagram: `
flowchart TD
  User -->|message| Agent
  Agent -->|thought| LLM
  LLM -->|tool_call| ToolNode
  ToolNode -->|patient lookup| PatientDB
  ToolNode -->|schedule| CalendarAPI
  ToolNode -->|drug check| DrugDB
  ToolNode -->|billing calc| BillingService
  ToolNode -->|result| LLM
  LLM -->|tools_condition| Decision{More tools?}
  Decision -->|yes| LLM
  Decision -->|no - final| User
  `,
  concepts: [
    {
      id: "tool-decorator",
      title: "@tool Decorator",
      explanation:
        "The @tool decorator converts a Python function into a LangChain tool. The function's docstring becomes the tool description that the LLM reads to decide when to call it.",
      code: {
        language: "python",
        filename: "tools/patient_tools.py",
        snippet: `from langchain_core.tools import tool
from pydantic import BaseModel, Field

class GetPatientInput(BaseModel):
    patient_id: str = Field(description="The patient's unique identifier (e.g. P001)")

@tool("get_patient_by_id", args_schema=GetPatientInput)
def get_patient_by_id(patient_id: str) -> dict:
    """Retrieve complete patient information by their ID.
    Use this when the user asks about a specific patient."""
    patient = PATIENTS_DB.get(patient_id)
    if not patient:
        return {"error": f"Patient {patient_id} not found"}
    return patient`,
      },
      glossaryTerms: ["Tool Calling", "Function Calling", "ReAct"],
    },
    {
      id: "tool-node",
      title: "LangGraph ToolNode",
      explanation:
        "ToolNode automatically executes whichever tools the LLM calls. It reads tool_calls from the last AI message and returns ToolMessages with the results.",
      code: {
        language: "python",
        filename: "agent/graph.py",
        snippet: `from langgraph.prebuilt import ToolNode, tools_condition

tool_node = ToolNode(ALL_TOOLS)

graph = StateGraph(AgentState)
graph.add_node("llm", llm_node)
graph.add_node("tools", tool_node)

graph.add_edge(START, "llm")
graph.add_conditional_edges(
    "llm",
    tools_condition,  # Routes to "tools" if tool_calls present
)
graph.add_edge("tools", "llm")  # Loop back after tool execution`,
      },
      glossaryTerms: ["ToolNode", "tools_condition", "LangGraph"],
    },
    {
      id: "bind-tools",
      title: "Binding Tools to LLM",
      explanation:
        "llm.bind_tools() sends the tool schemas to the LLM in the API call so it can decide which tools to call.",
      code: {
        language: "python",
        filename: "agent/react_agent.py",
        snippet: `from tools import ALL_TOOLS

# Bind all 13 tools to the LLM
llm_with_tools = llm.bind_tools(ALL_TOOLS)

# The LLM now returns AIMessage with tool_calls
# when it decides to use a tool
async def llm_node(state: AgentState):
    response = await llm_with_tools.ainvoke(state["messages"])
    return {"messages": [response]}`,
      },
    },
  ],
  steps: [
    { number: 1, title: "Create patient tools (2)", description: "get_patient_by_id, search_patients_by_name" },
    { number: 2, title: "Create appointment tools (2)", description: "schedule_appointment, check_doctor_availability" },
    { number: 3, title: "Create billing tools (3)", description: "get_invoice_by_id, calculate_bill, apply_discount" },
    { number: 4, title: "Create medical tools (3)", description: "search_drug_interactions, lookup_icd10_code, get_drug_information" },
    { number: 5, title: "Create utility tools (3)", description: "get_current_datetime, calculate_patient_age, format_medical_date" },
    { number: 6, title: "Build ReAct agent graph", description: "Wire LLM + ToolNode loop with tools_condition routing." },
    { number: 7, title: "Test tool execution trace", description: "Verify tool_calls appear in response and ToolMessages are returned." },
  ],
  acceptanceCriteria: [
    { id: "ac1", text: "Agent calls get_patient_by_id for patient questions" },
    { id: "ac2", text: "Agent detects and reports drug interactions" },
    { id: "ac3", text: "calculate_bill applies 80/20 insurance split correctly" },
    { id: "ac4", text: "GET /tools lists all 13 tools with name and description" },
    { id: "ac5", text: "Agent loops correctly until no more tool calls needed" },
  ],
  gotchas: [
    {
      error: "Tool not called despite relevant query",
      cause: "Tool description is too vague for the LLM to recognise when to use it",
      fix: "Make tool docstrings explicit about when to use them — include trigger phrases",
    },
    {
      error: "ToolException: Tool X not found",
      cause: "Tool name in bind_tools doesn't match @tool decorator name",
      fix: "Pass the same tool instances to both bind_tools() and ToolNode()",
    },
  ],
  resources: [
    { title: "LangGraph Tool Calling", url: "https://langchain-ai.github.io/langgraph/how-tos/tool-calling/" },
    { title: "LangChain Tools", url: "https://python.langchain.com/docs/concepts/tools/" },
  ],
};
