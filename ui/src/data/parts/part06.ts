import type { PartData } from "../../types";

export const part06: PartData = {
  id: "06",
  title: "Multi-Agent Orchestration",
  goal: "Build a supervisor agent that routes tasks to specialised subagents for triage, billing, and records.",
  phase: 3,
  phaseLabel: "Multi-Agent Systems",
  folder: "part_06_multi_agent",
  estimatedHours: 5,
  difficulty: "intermediate",
  prerequisites: ["01", "02", "03", "04", "05"],
  unlocks: ["07"],
  whatYouBuild: [
    { label: "POST /supervisor/chat", description: "Submit query to supervisor router" },
    { label: "GET /agents", description: "List all available specialised agents" },
    { label: "GET /supervisor/sessions/{id}", description: "Get session with routing history" },
  ],
  mermaidDiagram: `
flowchart TD
  User -->|query| Supervisor
  Supervisor -->|classify intent| Router

  Router -->|triage intent| TriageAgent
  Router -->|billing intent| BillingAgent
  Router -->|records intent| RecordsAgent
  Router -->|general intent| GeneralAgent

  TriageAgent -->|result| Supervisor
  BillingAgent -->|result| Supervisor
  RecordsAgent -->|result| Supervisor
  GeneralAgent -->|result| Supervisor

  Supervisor -->|final answer| User
  `,
  concepts: [
    {
      id: "supervisor-pattern",
      title: "Supervisor Pattern",
      explanation:
        "A supervisor LLM routes tasks to worker agents based on intent. The supervisor reads worker outputs and decides when the task is complete or needs another worker.",
      code: {
        language: "python",
        filename: "agents/supervisor.py",
        snippet: `SUPERVISOR_PROMPT = """You are a hospital AI supervisor.
Route the user's request to the appropriate specialist:
- triage: symptoms, medical advice, urgency assessment
- billing: invoices, payments, insurance
- records: patient history, test results, prescriptions
- general: hospital info, directions, visiting hours

Respond with JSON: {"next": "triage|billing|records|general|FINISH"}"""

supervisor_chain = (
    ChatPromptTemplate.from_messages([
        ("system", SUPERVISOR_PROMPT),
        MessagesPlaceholder("messages"),
    ])
    | llm.with_structured_output(RouterOutput)
)`,
      },
      glossaryTerms: ["Supervisor Pattern", "Multi-Agent", "Intent Classification"],
    },
    {
      id: "worker-agents",
      title: "Specialised Worker Agents",
      explanation:
        "Each worker is an independent LangGraph subgraph compiled with its own prompt, tools, and state. Workers communicate results back via the shared state.",
      code: {
        language: "python",
        filename: "agents/graph.py",
        snippet: `from langgraph.graph import StateGraph, START, END

def make_agent_node(agent_name: str, system_prompt: str):
    """Factory that creates a worker subgraph."""
    chain = (
        ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder("messages"),
        ])
        | llm
    )
    async def node(state: MultiAgentState):
        result = await chain.ainvoke(state)
        return {"messages": [result], "last_agent": agent_name}
    return node`,
      },
    },
  ],
  steps: [
    { number: 1, title: "Define MultiAgentState", description: "Add 'next' router field and 'last_agent' tracking to state." },
    { number: 2, title: "Build specialised agents", description: "Create triage, billing, records, and general agent nodes with targeted system prompts." },
    { number: 3, title: "Build the supervisor node", description: "Supervisor uses structured output to decide which agent handles the request." },
    { number: 4, title: "Wire the orchestration graph", description: "Supervisor → workers → supervisor loop with FINISH terminal condition." },
    { number: 5, title: "Add session persistence", description: "Use SqliteSaver for durable multi-session state." },
  ],
  acceptanceCriteria: [
    { id: "ac1", text: "Billing questions route to the billing agent" },
    { id: "ac2", text: "Supervisor correctly identifies FINISH after a worker responds" },
    { id: "ac3", text: "Session history shows which agent handled each turn" },
    { id: "ac4", text: "Ambiguous queries ask for clarification before routing" },
  ],
  gotchas: [
    {
      error: "Infinite loop: supervisor always routes to same agent",
      cause: "Worker result not added to messages before supervisor re-runs",
      fix: "Ensure worker node appends its AIMessage to state['messages']",
    },
  ],
  resources: [
    { title: "LangGraph Multi-Agent Supervisor", url: "https://langchain-ai.github.io/langgraph/tutorials/multi_agent/agent_supervisor/" },
  ],
};
