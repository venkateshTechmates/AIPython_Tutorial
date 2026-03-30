"""Part 9 — FastAPI application for Human-in-the-Loop workflows."""

import sys
from contextlib import asynccontextmanager
from typing import Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.messages import HumanMessage
from pydantic import BaseModel

sys.path.append("..")

from approval.approval_store import get_approval_store, ApprovalStatus

# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class StartPrescriptionRequest(BaseModel):
    patient_id: str
    drug_name: str
    dosage: str
    prescriber: str


class StartBillingRequest(BaseModel):
    patient_id: str
    invoice_id: str
    total_amount: float
    insurance_plan: str
    procedures: Optional[list[str]] = None


class StartDischargeRequest(BaseModel):
    patient_id: str
    admitting_diagnosis: str
    discharge_diagnosis: str
    length_of_stay_days: int
    discharge_medications: Optional[list[str]] = None
    follow_up_required: bool = True


class ResolveApprovalRequest(BaseModel):
    approved: bool
    resolved_by: str
    reason: Optional[str] = None
    # workflow-specific fields
    amendments: Optional[str] = None   # discharge: physician amendments
    reviewed: Optional[bool] = None    # discharge: nurse reviewed flag
    cleared: Optional[bool] = None     # discharge: pharmacy cleared flag


class WorkflowStartResponse(BaseModel):
    thread_id: str
    status: str
    next_action: str
    approval_id: Optional[str] = None


# ---------------------------------------------------------------------------
# App lifecycle
# ---------------------------------------------------------------------------

_llm = None
_prescription_graph = None
_billing_graph = None
_discharge_graph = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _llm, _prescription_graph, _billing_graph, _discharge_graph
    try:
        from langchain_openai import ChatOpenAI
        from workflows.prescription_workflow import build_prescription_workflow
        from workflows.billing_workflow import build_billing_workflow
        from workflows.discharge_workflow import build_discharge_workflow

        _llm = ChatOpenAI(model="gpt-4o", temperature=0)
        _prescription_graph = build_prescription_workflow(_llm)
        _billing_graph = build_billing_workflow(_llm)
        _discharge_graph = build_discharge_workflow(_llm)
    except Exception:
        pass
    yield


app = FastAPI(
    title="Hospital Human-in-the-Loop Workflows",
    description="Part 9 — Prescription, billing, and discharge workflows with human approval",
    version="0.9.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def _require_graph(graph):
    if graph is None:
        raise HTTPException(status_code=503, detail="Workflow not available — check OPENAI_API_KEY.")


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/")
async def root():
    return {
        "part": 9,
        "title": "Human-in-the-Loop Workflows",
        "workflows": ["prescription", "billing", "discharge"],
        "endpoints": {
            "start_prescription": "POST /workflow/prescription/start",
            "start_billing": "POST /workflow/billing/start",
            "start_discharge": "POST /workflow/discharge/start",
            "resolve_approval": "POST /approvals/{approval_id}/resolve",
            "list_pending": "GET /approvals/pending",
            "health": "GET /health",
        },
    }


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "workflows_ready": all([_prescription_graph, _billing_graph, _discharge_graph]),
    }


@app.post("/workflow/prescription/start", response_model=WorkflowStartResponse)
async def start_prescription(request: StartPrescriptionRequest):
    """Start a prescription review workflow. Pauses for human pharmacist approval."""
    _require_graph(_prescription_graph)
    thread_id = str(uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    initial_state = {
        "messages": [],
        "patient_id": request.patient_id,
        "drug_name": request.drug_name,
        "dosage": request.dosage,
        "prescriber": request.prescriber,
        "ai_recommendation": "",
        "human_decision": "pending",
        "rejection_reason": "",
        "workflow_complete": False,
    }

    result = await _prescription_graph.ainvoke(initial_state, config=config)
    store = get_approval_store()
    approval = store.create(
        workflow_type="prescription",
        thread_id=thread_id,
        payload={
            "patient_id": request.patient_id,
            "drug_name": request.drug_name,
            "dosage": request.dosage,
            "ai_recommendation": result.get("ai_recommendation", ""),
        },
    )
    return WorkflowStartResponse(
        thread_id=thread_id,
        status="awaiting_human_review",
        next_action="POST /approvals/{approval_id}/resolve",
        approval_id=approval.approval_id,
    )


@app.post("/workflow/billing/start", response_model=WorkflowStartResponse)
async def start_billing(request: StartBillingRequest):
    """Start a billing authorization workflow. May require human review for high-value claims."""
    _require_graph(_billing_graph)
    thread_id = str(uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    initial_state = {
        "messages": [],
        "patient_id": request.patient_id,
        "invoice_id": request.invoice_id,
        "total_amount": request.total_amount,
        "insurance_plan": request.insurance_plan,
        "procedures": request.procedures or [],
        "ai_assessment": "",
        "authorization_status": "pending",
        "override_reason": "",
        "workflow_complete": False,
    }

    result = await _billing_graph.ainvoke(initial_state, config=config)
    if result.get("workflow_complete"):
        return WorkflowStartResponse(
            thread_id=thread_id,
            status=result.get("authorization_status", "unknown"),
            next_action="completed",
        )

    store = get_approval_store()
    approval = store.create(
        workflow_type="billing",
        thread_id=thread_id,
        payload={
            "invoice_id": request.invoice_id,
            "total_amount": request.total_amount,
            "ai_assessment": result.get("ai_assessment", ""),
        },
    )
    return WorkflowStartResponse(
        thread_id=thread_id,
        status="awaiting_billing_authorization",
        next_action="POST /approvals/{approval_id}/resolve",
        approval_id=approval.approval_id,
    )


@app.post("/workflow/discharge/start", response_model=WorkflowStartResponse)
async def start_discharge(request: StartDischargeRequest):
    """Start a patient discharge workflow requiring physician, nurse, and pharmacy sign-offs."""
    _require_graph(_discharge_graph)
    thread_id = str(uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    initial_state = {
        "messages": [],
        "patient_id": request.patient_id,
        "admitting_diagnosis": request.admitting_diagnosis,
        "discharge_diagnosis": request.discharge_diagnosis,
        "length_of_stay_days": request.length_of_stay_days,
        "discharge_medications": request.discharge_medications or [],
        "follow_up_required": request.follow_up_required,
        "discharge_summary": "",
        "physician_signed": False,
        "nurse_reviewed": False,
        "pharmacy_cleared": False,
        "discharge_ready": False,
        "workflow_complete": False,
    }

    result = await _discharge_graph.ainvoke(initial_state, config=config)
    store = get_approval_store()
    approval = store.create(
        workflow_type="discharge",
        thread_id=thread_id,
        payload={
            "patient_id": request.patient_id,
            "discharge_summary": result.get("discharge_summary", ""),
            "step": "physician_signoff",
        },
    )
    return WorkflowStartResponse(
        thread_id=thread_id,
        status="awaiting_physician_signoff",
        next_action="POST /approvals/{approval_id}/resolve",
        approval_id=approval.approval_id,
    )


@app.post("/approvals/{approval_id}/resolve")
async def resolve_approval(approval_id: str, request: ResolveApprovalRequest):
    """Resolve a pending approval decision and resume the workflow."""
    store = get_approval_store()
    approval = store.get(approval_id)
    if approval is None:
        raise HTTPException(status_code=404, detail="Approval not found or expired.")
    if approval.status != ApprovalStatus.PENDING:
        raise HTTPException(status_code=409, detail=f"Approval is already {approval.status.value}.")

    # Build the resolution payload for workflow resumption
    resolution: dict = {
        "approved": request.approved,
        "reason": request.reason or "",
    }
    if request.amendments:
        resolution["amendments"] = request.amendments
    if request.reviewed is not None:
        resolution["reviewed"] = request.reviewed
    if request.cleared is not None:
        resolution["cleared"] = request.cleared

    store.resolve(approval_id, request.approved, request.resolved_by, resolution)

    # Resume the appropriate graph
    graph = {
        "prescription": _prescription_graph,
        "billing": _billing_graph,
        "discharge": _discharge_graph,
    }.get(approval.workflow_type)

    if graph is None:
        raise HTTPException(status_code=503, detail="Workflow graph not loaded.")

    config = {"configurable": {"thread_id": approval.thread_id}}

    # Map resolution to the interrupt payload the graph expects
    if approval.workflow_type == "prescription":
        resume_value = {"decision": "approved" if request.approved else "rejected", "reason": request.reason or ""}
    elif approval.workflow_type == "billing":
        resume_value = {"authorized": request.approved, "reason": request.reason or ""}
    else:
        # Discharge — payload depends on which step was interrupted
        step = approval.payload.get("step", "physician_signoff")
        if step == "physician_signoff":
            resume_value = {"signed": request.approved, "amendments": request.amendments or ""}
        elif step == "nurse_review":
            resume_value = {"reviewed": request.reviewed if request.reviewed is not None else request.approved}
        else:
            resume_value = {"cleared": request.cleared if request.cleared is not None else request.approved}

    result = await graph.ainvoke(Command(resume=resume_value), config=config)

    return {
        "approval_id": approval_id,
        "workflow_type": approval.workflow_type,
        "thread_id": approval.thread_id,
        "resolution": "approved" if request.approved else "rejected",
        "workflow_complete": result.get("workflow_complete", False),
        "final_status": result.get(
            "authorization_status",
            result.get("human_decision", result.get("discharge_ready", "unknown")),
        ),
    }


@app.get("/approvals/pending")
async def list_pending_approvals(workflow_type: Optional[str] = None):
    """List all pending human approvals."""
    store = get_approval_store()
    pending = store.list_pending(workflow_type)
    return {
        "pending": [
            {
                "approval_id": r.approval_id,
                "workflow_type": r.workflow_type,
                "thread_id": r.thread_id,
                "payload": r.payload,
                "created_at": r.created_at,
                "status": r.status.value,
            }
            for r in pending
        ],
        "total": len(pending),
    }
