"""Part 9 — Tests for HITL workflows and approval store."""

import pytest
import time
from unittest.mock import patch, MagicMock, AsyncMock


# ---------------------------------------------------------------------------
# Approval store tests
# ---------------------------------------------------------------------------

class TestApprovalStore:
    def setup_method(self):
        from approval.approval_store import ApprovalStore
        self.store = ApprovalStore()

    def test_create_and_get(self):
        req = self.store.create("prescription", "thread-001", {"drug_name": "aspirin"})
        assert req.approval_id is not None
        fetched = self.store.get(req.approval_id)
        assert fetched is not None
        assert fetched.workflow_type == "prescription"

    def test_resolve_approve(self):
        req = self.store.create("billing", "thread-002", {"total": 500})
        resolved = self.store.resolve(req.approval_id, True, "Dr. Smith", {"note": "ok"})
        assert resolved.status.value == "approved"
        assert resolved.resolved_by == "Dr. Smith"

    def test_resolve_reject(self):
        req = self.store.create("prescription", "thread-003", {})
        resolved = self.store.resolve(req.approval_id, False, "pharmacist", {"reason": "wrong dose"})
        assert resolved.status.value == "rejected"

    def test_cannot_resolve_twice(self):
        req = self.store.create("discharge", "thread-004", {})
        self.store.resolve(req.approval_id, True, "nurse")
        second = self.store.resolve(req.approval_id, False, "nurse")
        assert second is None  # can't resolve twice

    def test_expired_returns_expired_status(self):
        from approval.approval_store import ApprovalStore
        store = ApprovalStore(ttl_seconds=0)
        req = store.create("prescription", "thread-exp", {})
        time.sleep(0.01)
        fetched = store.get(req.approval_id)
        assert fetched.status.value == "expired"

    def test_list_pending_filtered(self):
        self.store.create("prescription", "t-p1", {})
        self.store.create("billing", "t-b1", {})
        pending_rx = self.store.list_pending("prescription")
        assert all(r.workflow_type == "prescription" for r in pending_rx)

    def test_list_pending_all(self):
        self.store.create("prescription", "t-all1", {})
        self.store.create("billing", "t-all2", {})
        all_pending = self.store.list_pending()
        assert len(all_pending) >= 2

    def test_get_missing_returns_none(self):
        assert self.store.get("non-existent-id") is None


# ---------------------------------------------------------------------------
# Workflow graph tests (mocked LLM)
# ---------------------------------------------------------------------------

class TestPrescriptionWorkflow:
    @pytest.fixture
    def mock_llm(self):
        llm = MagicMock()
        llm.invoke = MagicMock(return_value=MagicMock(content="APPROVE — Dosage within normal range."))
        return llm

    def test_workflow_builds(self, mock_llm):
        from workflows.prescription_workflow import build_prescription_workflow
        graph = build_prescription_workflow(mock_llm)
        assert graph is not None

    @pytest.mark.asyncio
    async def test_workflow_pauses_for_review(self, mock_llm):
        from workflows.prescription_workflow import build_prescription_workflow
        graph = build_prescription_workflow(mock_llm)
        config = {"configurable": {"thread_id": "test-rx-001"}}

        initial_state = {
            "messages": [],
            "patient_id": "P001",
            "drug_name": "Lisinopril",
            "dosage": "10mg daily",
            "prescriber": "Dr. Patel",
            "ai_recommendation": "",
            "human_decision": "pending",
            "rejection_reason": "",
            "workflow_complete": False,
        }

        # Should pause at the interrupt
        result = await graph.ainvoke(initial_state, config=config)
        # After first invoke, workflow should be interrupted (not complete)
        assert not result.get("workflow_complete", False)


class TestBillingWorkflow:
    @pytest.fixture
    def mock_llm(self):
        llm = MagicMock()
        llm.invoke = MagicMock(return_value=MagicMock(content="AUTO_APPROVE — Standard procedures covered."))
        return llm

    def test_workflow_builds(self, mock_llm):
        from workflows.billing_workflow import build_billing_workflow
        graph = build_billing_workflow(mock_llm)
        assert graph is not None

    @pytest.mark.asyncio
    async def test_low_value_auto_approves(self, mock_llm):
        from workflows.billing_workflow import build_billing_workflow
        graph = build_billing_workflow(mock_llm)
        config = {"configurable": {"thread_id": "test-bill-001"}}

        state = {
            "messages": [],
            "patient_id": "P002",
            "invoice_id": "INV-0001",
            "total_amount": 200.0,  # below threshold
            "insurance_plan": "BlueCross Basic",
            "procedures": ["office_visit"],
            "ai_assessment": "",
            "authorization_status": "pending",
            "override_reason": "",
            "workflow_complete": False,
        }

        result = await graph.ainvoke(state, config=config)
        assert result.get("workflow_complete") is True
        assert result.get("authorization_status") == "authorized"


class TestDischargeWorkflow:
    @pytest.fixture
    def mock_llm(self):
        llm = MagicMock()
        llm.invoke = MagicMock(return_value=MagicMock(
            content="Patient discharged in stable condition. Follow-up in 2 weeks."
        ))
        return llm

    def test_workflow_builds(self, mock_llm):
        from workflows.discharge_workflow import build_discharge_workflow
        graph = build_discharge_workflow(mock_llm)
        assert graph is not None

    @pytest.mark.asyncio
    async def test_workflow_generates_summary_and_pauses(self, mock_llm):
        from workflows.discharge_workflow import build_discharge_workflow
        graph = build_discharge_workflow(mock_llm)
        config = {"configurable": {"thread_id": "test-dis-001"}}

        state = {
            "messages": [],
            "patient_id": "P003",
            "admitting_diagnosis": "Chest pain",
            "discharge_diagnosis": "Unstable angina",
            "length_of_stay_days": 3,
            "discharge_medications": ["aspirin 81mg", "metoprolol 25mg"],
            "follow_up_required": True,
            "discharge_summary": "",
            "physician_signed": False,
            "nurse_reviewed": False,
            "pharmacy_cleared": False,
            "discharge_ready": False,
            "workflow_complete": False,
        }

        result = await graph.ainvoke(state, config=config)
        # Should have a discharge summary but not be complete (paused for physician)
        assert result.get("discharge_summary") != ""
        assert not result.get("workflow_complete", False)
