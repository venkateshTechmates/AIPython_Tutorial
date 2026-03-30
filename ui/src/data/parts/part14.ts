import type { PartData } from "../../types";

export const part14: PartData = {
  id: "14",
  title: "Capstone — Full Platform",
  goal: "Integrate all 13 parts into one unified Hospital Intelligence Platform with intent routing, RAG, tools, memory, and streaming.",
  phase: 5,
  phaseLabel: "Capstone",
  folder: "part_14_capstone",
  estimatedHours: 8,
  difficulty: "advanced",
  prerequisites: ["01","02","03","04","05","06","07","08","09","10","11","12","13"],
  unlocks: [],
  whatYouBuild: [
    { label: "POST /platform/chat", description: "Full patient journey — intent routes to right agent" },
    { label: "POST /platform/chat (stream)", description: "Streaming version via SSE" },
    { label: "POST /platform/memory", description: "Save long-term patient memory" },
    { label: "GET /platform/patient/{id}/memory", description: "Retrieve all patient memory" },
    { label: "GET /health", description: "Platform health check" },
  ],
  mermaidDiagram: `
flowchart TD
  User -->|POST /platform/chat| FastAPI
  FastAPI --> inject_context
  inject_context -->|MemoryManager| classify_intent

  classify_intent -->|is_emergency: true| emergency_escalation
  classify_intent -->|appointment/billing/records| tool_calling_node
  classify_intent -->|general/unknown| rag_retrieval

  emergency_escalation -->|urgency_level=1| END
  tool_calling_node -->|tool loop| ToolNode
  ToolNode --> tool_calling_node
  tool_calling_node --> synthesize_response
  rag_retrieval --> synthesize_response
  synthesize_response --> END

  style emergency_escalation fill:#ef4444
  style inject_context fill:#6366f1
  style classify_intent fill:#8b5cf6
  `,
  concepts: [
    {
      id: "capstone-state",
      title: "PatientJourneyState",
      explanation:
        "The capstone state combines all parts: messages, memory context, intent, urgency, tool results, RAG context, workflow tracking, and emergency flags.",
      code: {
        language: "python",
        filename: "platform/state.py",
        snippet: `from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

class PatientJourneyState(TypedDict):
    # Core conversation
    messages: Annotated[list, add_messages]
    session_id: str
    patient_id: str | None

    # Intent classification (Part 5/6)
    intent: str | None
    intent_confidence: float
    is_emergency: bool

    # Tool results (Part 7)
    tool_results: list[dict]

    # RAG context (Part 4)
    rag_context: str
    rag_sources: list[str]

    # Memory (Part 8)
    patient_context: str
    context_injected: bool

    # Urgency (Part 5)
    urgency_level: int | None
    urgency_label: str

    # Final output
    final_response: str
    error: str | None`,
      },
      glossaryTerms: ["State", "TypedDict", "LangGraph"],
    },
    {
      id: "capstone-routing",
      title: "Unified Intent Router",
      explanation:
        "The classify_intent node uses GPT-4o to categorise the query, then route_after_classification maps intent to the right subgraph branch.",
      code: {
        language: "python",
        filename: "platform/graph.py",
        snippet: `def route_after_classification(state: PatientJourneyState) -> str:
    if state.get("is_emergency"):
        return "emergency"
    intent = state.get("intent", "general")
    if intent in ("appointment", "billing", "records"):
        return "tools"
    return "rag"

graph.add_conditional_edges(
    "classify_intent",
    route_after_classification,
    {
        "emergency": "emergency_escalation",
        "tools":     "tool_calling_node",
        "rag":       "rag_retrieval",
    }
)`,
      },
    },
  ],
  steps: [
    { number: 1, title: "Define PatientJourneyState", description: "Master TypedDict merging fields from all 13 parts." },
    { number: 2, title: "Implement inject_patient_context node", description: "Load MemoryManager and prepend patient context as system message." },
    { number: 3, title: "Implement classify_intent node", description: "GPT-4o JSON output: intent, confidence, is_emergency." },
    { number: 4, title: "Implement emergency_escalation node", description: "Immediate response, urgency_level=1, skip all other nodes." },
    { number: 5, title: "Wire tool_calling_node + ToolNode loop", description: "Import ALL_TOOLS from Part 7, bind to LLM, loop until no more calls." },
    { number: 6, title: "Implement rag_retrieval and synthesize_response nodes", description: "Retrieve from Part 4, synthesise final answer." },
    { number: 7, title: "Compile capstone graph and wire FastAPI", description: "POST /platform/chat handles both streaming and non-streaming modes." },
  ],
  acceptanceCriteria: [
    { id: "ac1", text: "Emergency queries route directly to emergency_escalation node" },
    { id: "ac2", text: "Appointment queries invoke the schedule_appointment tool" },
    { id: "ac3", text: "General queries use RAG over hospital documents" },
    { id: "ac4", text: "Patient context is injected from Part 8 memory" },
    { id: "ac5", text: "Streaming mode emits tokens via SSE" },
    { id: "ac6", text: "All tests in tests/test_capstone.py pass" },
  ],
  gotchas: [
    {
      error: "ImportError: cannot import from part_07_tool_calling",
      cause: "sys.path doesn't include the parent directory",
      fix: "Add sys.path.insert(0, '../part_07_tool_calling') before the import in platform/graph.py",
    },
    {
      error: "Graph produces empty final_response",
      cause: "synthesize_response node not writing to final_response key",
      fix: "Return {'final_response': llm_response.content} from the synthesize node",
    },
  ],
  resources: [
    { title: "LangGraph Full Example", url: "https://langchain-ai.github.io/langgraph/tutorials/" },
    { title: "Part 14 GitHub Source", url: "https://github.com/your-org/hospital-ai-platform/tree/main/part_14_capstone" },
  ],
};
