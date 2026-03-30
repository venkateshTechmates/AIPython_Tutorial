import type { PartData } from "../../types";

export const part09: PartData = {
  id: "09",
  title: "Human-in-the-Loop",
  goal: "Build clinical approval workflows where LangGraph pauses execution for human review before proceeding.",
  phase: 4,
  phaseLabel: "Production Patterns",
  folder: "part_09_human_in_loop",
  estimatedHours: 5,
  difficulty: "advanced",
  prerequisites: ["05", "06", "07", "08"],
  unlocks: ["10"],
  whatYouBuild: [
    { label: "POST /workflow/prescription/start", description: "Start prescription approval" },
    { label: "POST /workflow/billing/start", description: "Start billing review workflow" },
    { label: "POST /workflow/discharge/start", description: "Initiate discharge sign-off" },
    { label: "POST /approvals/{id}/resolve", description: "Approve or reject a pending item" },
    { label: "GET /approvals/pending", description: "List all pending approvals" },
  ],
  mermaidDiagram: `
stateDiagram-v2
  [*] --> analyze_prescription
  analyze_prescription --> human_review : AI analysis complete
  human_review --> [*] : interrupted — waiting for human

  state human_review {
    [*] --> waiting
    waiting --> approved : doctor approves
    waiting --> rejected : doctor rejects
    approved --> [*]
    rejected --> [*]
  }

  human_review --> finalize : approved
  human_review --> reject_prescription : rejected
  finalize --> [*]
  reject_prescription --> [*]
  `,
  concepts: [
    {
      id: "interrupt",
      title: "interrupt() — Pausing Graph Execution",
      explanation:
        "interrupt() halts the graph at any node and saves the checkpoint. The graph resumes exactly where it stopped when you call graph.ainvoke(Command(resume=value)).",
      code: {
        language: "python",
        filename: "workflows/prescription_workflow.py",
        snippet: `from langgraph.types import interrupt, Command

async def human_review_node(state: PrescriptionState):
    # Pause here and emit the payload to the caller
    human_decision = interrupt({
        "approval_type": "prescription",
        "drug": state["drug_name"],
        "dose": state["dosage"],
        "ai_analysis": state["ai_analysis"],
        "risk_flags": state["risk_flags"],
    })
    # Execution resumes here after approval
    return {
        "approved": human_decision["approved"],
        "reviewer": human_decision["reviewer_id"],
    }`,
      },
      glossaryTerms: ["HITL", "interrupt", "Checkpoint"],
    },
    {
      id: "resume-command",
      title: "Resuming with Command",
      explanation:
        "After a human decision is made, the graph resumes from the checkpoint by passing Command(resume=value) as input instead of the full state.",
      code: {
        language: "python",
        filename: "main.py",
        snippet: `from langgraph.types import Command

@app.post("/approvals/{approval_id}/resolve")
async def resolve_approval(
    approval_id: str,
    decision: ApprovalDecision
):
    approval = approval_store.get(approval_id)
    config = {"configurable": {"thread_id": approval.thread_id}}

    # Resume the paused graph with the human decision
    result = await workflow_graph.ainvoke(
        Command(resume={
            "approved": decision.approved,
            "reviewer_id": decision.reviewer_id,
            "notes": decision.notes,
        }),
        config=config
    )
    return result`,
      },
      glossaryTerms: ["Command", "Resume", "LangGraph"],
    },
  ],
  steps: [
    { number: 1, title: "Build prescription workflow", description: "analyze → interrupt(human_review) → finalize/reject." },
    { number: 2, title: "Build billing approval workflow", description: "Auto-approve < $1000, interrupt > $5000, AI-assess middle tier." },
    { number: 3, title: "Build discharge workflow", description: "Three sequential interrupts: physician, nurse, pharmacy." },
    { number: 4, title: "Build ApprovalStore", description: "Track pending approvals with UUID, TTL, and thread_id reference." },
    { number: 5, title: "Wire POST /approvals/{id}/resolve", description: "Resume the paused graph with Command(resume=decision)." },
  ],
  acceptanceCriteria: [
    { id: "ac1", text: "Prescription workflow pauses at human_review node" },
    { id: "ac2", text: "Approved prescriptions complete the finalize node" },
    { id: "ac3", text: "Billing auto-approves invoices under $1000" },
    { id: "ac4", text: "Discharge requires three sequential human sign-offs" },
    { id: "ac5", text: "Expired (>24h) approval requests return 410 Gone" },
  ],
  gotchas: [
    {
      error: "Graph doesn't resume after Command(resume=...) call",
      cause: "interrupt_before not set on the node that contains interrupt()",
      fix: "Pass interrupt_before=['human_review'] to graph.compile()",
    },
  ],
  resources: [
    { title: "LangGraph Human-in-the-Loop", url: "https://langchain-ai.github.io/langgraph/concepts/human_in_the_loop/" },
    { title: "interrupt() API", url: "https://langchain-ai.github.io/langgraph/reference/types/#langgraph.types.interrupt" },
  ],
};
