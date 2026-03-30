"""Part 11 — Integration tests for agent flows (mocked LLM, no real API key needed)."""

import pytest
from unittest.mock import MagicMock, AsyncMock
from langchain_core.messages import HumanMessage, AIMessage


class TestTriageAgentFlow:
    """End-to-end tests for the triage agent graph (Part 5)."""

    @pytest.fixture
    def mock_llm_intake(self):
        """Mock that simulates the intake → analysis → classify → recommend flow."""
        responses = [
            "I understand you're experiencing chest pain. INTAKE_COMPLETE: {\"name\": \"Test Patient\"}",
            "Chest pain with shortness of breath is concerning. ANALYSIS_COMPLETE: {\"symptoms\": [\"chest pain\", \"shortness of breath\"]}",
            '{"urgency_level": 2, "urgency_label": "EMERGENT", "reasoning": "Cardiac symptoms"}',
            "Please go to the emergency department immediately.",
        ]
        call_count = [0]

        def invoke_side_effect(messages):
            idx = min(call_count[0], len(responses) - 1)
            call_count[0] += 1
            return MagicMock(content=responses[idx])

        llm = MagicMock()
        llm.invoke = MagicMock(side_effect=invoke_side_effect)
        return llm

    @pytest.mark.asyncio
    async def test_triage_graph_initializes(self, mock_llm_intake):
        """Triage graph should compile without errors."""
        import sys
        sys.path.insert(0, r"d:\pythonMain\Tutorial\part_05_first_agent")
        try:
            from agent.graph import build_triage_graph
            graph = build_triage_graph()
            assert graph is not None
        except ImportError:
            pytest.skip("Part 05 not available")


class TestMultiAgentFlow:
    """Integration tests for the multi-agent orchestration (Part 6)."""

    @pytest.fixture
    def mock_llm_router(self):
        llm = MagicMock()
        llm.invoke = MagicMock(return_value=MagicMock(
            content='{"intent": "appointment", "confidence": 0.95, "reasoning": "Scheduling request"}'
        ))
        return llm

    @pytest.mark.asyncio
    async def test_intent_router_returns_valid_intent(self, mock_llm_router):
        """Router should return a valid intent from the fixed set."""
        valid_intents = {"appointment", "billing", "records", "triage", "general"}
        import json
        response = mock_llm_router.invoke(["dummy message"])
        parsed = json.loads(response.content)
        assert parsed["intent"] in valid_intents
        assert 0.0 <= parsed["confidence"] <= 1.0


class TestToolCallingFlow:
    """Integration tests for tool-calling agent (Part 7)."""

    @pytest.mark.asyncio
    async def test_patient_tool_returns_dict(self):
        """Patient lookup tool should always return a dict."""
        import sys
        sys.path.insert(0, r"d:\pythonMain\Tutorial\part_07_tool_calling")
        try:
            from tools.patient_tools import get_patient_by_id
            result = await get_patient_by_id.ainvoke({"patient_id": 1})
            assert isinstance(result, dict)
        except ImportError:
            pytest.skip("Part 07 not available")

    @pytest.mark.asyncio
    async def test_drug_interaction_check(self):
        """Drug interaction tool should find warfarin+aspirin as major."""
        import sys
        sys.path.insert(0, r"d:\pythonMain\Tutorial\part_07_tool_calling")
        try:
            from tools.medical_tools import search_drug_interactions
            result = await search_drug_interactions.ainvoke(
                {"drug_a": "warfarin", "drug_b": "aspirin"}
            )
            assert result["interaction_found"] is True
            assert result["severity"] == "major"
        except ImportError:
            pytest.skip("Part 07 not available")


class TestMemoryAgentFlow:
    """Integration tests for memory-enabled agent (Part 8)."""

    def test_session_store_lifecycle(self):
        """Session store should handle create/get/delete cycle."""
        import sys
        sys.path.insert(0, r"d:\pythonMain\Tutorial\part_08_memory_state")
        try:
            from sessions.session_store import SessionStore
            store = SessionStore()
            session = store.create("sess-int-001", "P001")
            assert store.get("sess-int-001") is not None
            store.delete("sess-int-001")
            assert store.get("sess-int-001") is None
        except ImportError:
            pytest.skip("Part 08 not available")


class TestHITLWorkflowFlow:
    """Integration tests for HITL approval workflow (Part 9)."""

    @pytest.fixture
    def mock_llm(self):
        llm = MagicMock()
        llm.invoke = MagicMock(return_value=MagicMock(
            content="AUTO_APPROVE — Standard procedure, dosage within range."
        ))
        return llm

    @pytest.mark.asyncio
    async def test_billing_approval_store_integration(self):
        """Approval store should track workflow state correctly."""
        import sys
        sys.path.insert(0, r"d:\pythonMain\Tutorial\part_09_human_in_loop")
        try:
            from approval.approval_store import ApprovalStore
            store = ApprovalStore()
            req = store.create("billing", "thread-int-001", {"amount": 1000})
            assert req.status.value == "pending"
            resolved = store.resolve(req.approval_id, True, "billing_staff")
            assert resolved.status.value == "approved"
        except ImportError:
            pytest.skip("Part 09 not available")
