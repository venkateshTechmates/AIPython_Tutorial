import type { PartData } from "../../types";

export const part05: PartData = {
  id: "05",
  title: "First LangGraph Agent",
  goal: "Build a stateful hospital triage agent using LangGraph StateGraph with multi-turn conversations.",
  phase: 2,
  phaseLabel: "RAG & First Agent",
  folder: "part_05_first_agent",
  estimatedHours: 4,
  difficulty: "intermediate",
  prerequisites: ["01", "02", "03", "04"],
  unlocks: ["06"],
  whatYouBuild: [
    { label: "POST /triage", description: "Start a new triage session" },
    { label: "POST /triage/{id}/message", description: "Send symptom message" },
    { label: "GET /triage/{id}/state", description: "Get current agent state" },
    { label: "GET /triage/{id}/history", description: "Full conversation history" },
  ],
  mermaidDiagram: `
stateDiagram-v2
  [*] --> intake
  intake --> symptom_analysis : patient describes symptoms
  symptom_analysis --> urgency_check : analysis complete
  urgency_check --> emergency_alert : score >= 8
  urgency_check --> schedule_appointment : 4 <= score < 8
  urgency_check --> self_care_advice : score < 4
  emergency_alert --> [*]
  schedule_appointment --> [*]
  self_care_advice --> [*]
  `,
  concepts: [
    {
      id: "state-graph",
      title: "LangGraph StateGraph",
      explanation:
        "StateGraph defines the agent as a directed graph where each node is a Python function that reads and writes to a shared state TypedDict. Edges define the flow between nodes.",
      code: {
        language: "python",
        filename: "agent/graph.py",
        snippet: `from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from agent.state import TriageState

graph = StateGraph(TriageState)

graph.add_node("intake", intake_node)
graph.add_node("symptom_analysis", analysis_node)
graph.add_node("urgency_check", urgency_node)

graph.add_edge(START, "intake")
graph.add_edge("intake", "symptom_analysis")
graph.add_conditional_edges(
    "urgency_check",
    route_by_urgency,
    {"high": "emergency_alert", "medium": "schedule", "low": "advice"}
)

# Compile with checkpointing for persistence
compiled = graph.compile(checkpointer=MemorySaver())`,
      },
      glossaryTerms: ["LangGraph", "StateGraph", "Checkpointing"],
    },
    {
      id: "agent-state",
      title: "Agent State TypedDict",
      explanation:
        "State is a TypedDict with Annotated[list, add_messages] for the messages field. add_messages is a reducer that appends new messages to the list instead of replacing it.",
      code: {
        language: "python",
        filename: "agent/state.py",
        snippet: `from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

class TriageState(TypedDict):
    messages: Annotated[list, add_messages]
    patient_id: str
    urgency_score: int | None
    urgency_label: str    # high / medium / low
    recommended_action: str
    session_id: str`,
      },
      glossaryTerms: ["TypedDict", "State Reducer", "add_messages"],
    },
    {
      id: "conditional-edges",
      title: "Conditional Edges (Routing)",
      explanation:
        "Conditional edges call a routing function that returns a string key, which maps to the next node. This is how the agent decides which path to take.",
      code: {
        language: "python",
        filename: "agent/graph.py",
        snippet: `def route_by_urgency(state: TriageState) -> str:
    score = state.get("urgency_score", 0)
    if score >= 8:
        return "high"
    elif score >= 4:
        return "medium"
    return "low"

graph.add_conditional_edges(
    "urgency_check",
    route_by_urgency,
    {"high": "emergency_alert",
     "medium": "schedule_appointment",
     "low": "self_care_advice"}
)`,
      },
      glossaryTerms: ["Conditional Edges", "Routing Function"],
    },
  ],
  steps: [
    { number: 1, title: "Define TriageState TypedDict", description: "Create state with messages (add_messages reducer), urgency_score, and session_id." },
    { number: 2, title: "Implement intake node", description: "Extract patient ID and chief complaint from the first message." },
    { number: 3, title: "Implement symptom analysis node", description: "Use GPT-4o to analyse symptoms and extract structured data." },
    { number: 4, title: "Implement urgency check node", description: "Score urgency 1–10 using structured LLM output with JSON mode." },
    { number: 5, title: "Add routing and terminal nodes", description: "Wire conditional edges and implement emergency/schedule/advice terminal nodes." },
    { number: 6, title: "Compile with MemorySaver", description: "Add checkpointing so conversation persists across API calls." },
    { number: 7, title: "Wire FastAPI endpoints", description: "Create POST /triage and POST /triage/{id}/message that pass thread_id as config." },
  ],
  acceptanceCriteria: [
    { id: "ac1", text: "Agent correctly routes high-urgency (≥8) cases to emergency alert" },
    { id: "ac2", text: "State is persisted across multi-turn conversations using thread_id" },
    { id: "ac3", text: "GET /triage/{id}/state returns current urgency score and label" },
    { id: "ac4", text: "Agent handles ambiguous symptoms with clarifying questions" },
  ],
  gotchas: [
    {
      error: "RecursionError: maximum graph depth exceeded",
      cause: "Missing END edge — agent cycles infinitely",
      fix: "Add graph.add_edge('terminal_node', END) for all terminal nodes",
    },
    {
      error: "KeyError on state access in node function",
      cause: "State field not initialised before first node runs",
      fix: "Provide default values in the initial state passed to graph.ainvoke()",
    },
  ],
  resources: [
    { title: "LangGraph Quickstart", url: "https://langchain-ai.github.io/langgraph/tutorials/introduction/" },
    { title: "LangGraph StateGraph API", url: "https://langchain-ai.github.io/langgraph/reference/graphs/" },
  ],
};
