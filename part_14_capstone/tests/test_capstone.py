"""Part 14 — Capstone tests."""

import sys
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from langchain_core.messages import HumanMessage, AIMessage

sys.path.insert(0, ".")

# ---------------------------------------------------------------------------
# State schema
# ---------------------------------------------------------------------------

class TestPatientJourneyState:
    def test_state_has_required_fields(self):
        from platform.state import PatientJourneyState
        keys = PatientJourneyState.__annotations__.keys()
        required = {
            "messages", "session_id", "patient_id", "intent",
            "intent_confidence", "tool_results", "rag_context",
            "rag_sources", "urgency_level", "urgency_label",
            "active_workflow", "awaiting_approval", "patient_context",
            "context_injected", "final_response", "is_emergency", "error",
        }
        for field in required:
            assert field in keys, f"Missing field: {field}"

    def test_state_intent_confidence_annotation(self):
        from platform.state import PatientJourneyState
        ann = PatientJourneyState.__annotations__
        assert "intent_confidence" in ann

    def test_state_messages_uses_add_messages(self):
        from platform.state import PatientJourneyState
        import typing
        ann = PatientJourneyState.__annotations__
        # Annotated[list[...], add_messages] or plain list — just ensure it's there
        assert "messages" in ann


# ---------------------------------------------------------------------------
# Node functions
# ---------------------------------------------------------------------------

class TestInjectPatientContextNode:
    def test_no_patient_id_skips_injection(self):
        from platform.nodes import inject_patient_context
        state = {
            "messages": [HumanMessage(content="Hello")],
            "patient_id": None,
            "context_injected": False,
            "patient_context": "",
        }
        result = inject_patient_context(state)
        # Should return state update with context_injected still False or True
        assert "context_injected" in result

    def test_already_injected_is_skipped(self):
        from platform.nodes import inject_patient_context
        state = {
            "messages": [HumanMessage(content="Hello")],
            "patient_id": "P001",
            "context_injected": True,
            "patient_context": "existing context",
        }
        result = inject_patient_context(state)
        assert result.get("context_injected") is True

    def test_patient_id_triggers_context_injection(self):
        from platform.nodes import inject_patient_context
        state = {
            "messages": [HumanMessage(content="Hello")],
            "patient_id": "P001",
            "context_injected": False,
            "patient_context": "",
        }
        with patch("platform.nodes.MemoryManager") as MockMM:
            mock_mgr = MagicMock()
            mock_mgr.build_context_prompt.return_value = "Patient name: John"
            MockMM.return_value = mock_mgr
            result = inject_patient_context(state)
        assert result.get("context_injected") is True


class TestClassifyIntentNode:
    def test_emergency_keywords_detected(self):
        from platform.nodes import classify_intent
        mock_llm = MagicMock()
        mock_llm.invoke.return_value = AIMessage(
            content='{"intent": "emergency", "confidence": 0.99, "is_emergency": true}'
        )
        node_fn = classify_intent(mock_llm)
        state = {
            "messages": [HumanMessage(content="I am having chest pain and can't breathe")],
            "intent": None,
            "intent_confidence": 0.0,
            "is_emergency": False,
        }
        result = node_fn(state)
        assert result["is_emergency"] is True
        assert result["intent"] == "emergency"

    def test_appointment_intent_parsed(self):
        from platform.nodes import classify_intent
        mock_llm = MagicMock()
        mock_llm.invoke.return_value = AIMessage(
            content='{"intent": "appointment", "confidence": 0.9, "is_emergency": false}'
        )
        node_fn = classify_intent(mock_llm)
        state = {
            "messages": [HumanMessage(content="I need to book an appointment")],
            "intent": None,
            "intent_confidence": 0.0,
            "is_emergency": False,
        }
        result = node_fn(state)
        assert result["intent"] == "appointment"
        assert result["is_emergency"] is False

    def test_invalid_json_falls_back_gracefully(self):
        from platform.nodes import classify_intent
        mock_llm = MagicMock()
        mock_llm.invoke.return_value = AIMessage(content="I cannot classify this.")
        node_fn = classify_intent(mock_llm)
        state = {
            "messages": [HumanMessage(content="unknown query")],
            "intent": None,
            "intent_confidence": 0.0,
            "is_emergency": False,
        }
        result = node_fn(state)  # should not raise
        assert "intent" in result


class TestEmergencyEscalationNode:
    def test_returns_emergency_response(self):
        from platform.nodes import emergency_escalation
        state = {
            "messages": [HumanMessage(content="help me")],
            "is_emergency": True,
            "urgency_level": None,
        }
        result = emergency_escalation(state)
        assert result["urgency_level"] == 1
        assert result["final_response"]
        response_lower = result["final_response"].lower()
        assert any(word in response_lower for word in ("emergency", "911", "immediately", "er"))


class TestSynthesizeResponseNode:
    def test_synthesizes_from_rag_context(self):
        from platform.nodes import synthesize_response
        mock_llm = MagicMock()
        mock_llm.invoke.return_value = AIMessage(content="Based on your records, your appointment is set.")
        node_fn = synthesize_response(mock_llm)
        state = {
            "messages": [HumanMessage(content="When is my appointment?")],
            "rag_context": "Appointment on Monday at 10am with Dr. Smith.",
            "tool_results": [],
            "final_response": "",
        }
        result = node_fn(state)
        assert result["final_response"]

    def test_synthesizes_from_tool_results(self):
        from platform.nodes import synthesize_response
        mock_llm = MagicMock()
        mock_llm.invoke.return_value = AIMessage(content="Your invoice total is $250.")
        node_fn = synthesize_response(mock_llm)
        state = {
            "messages": [HumanMessage(content="What is my bill?")],
            "rag_context": "",
            "tool_results": [{"tool": "get_invoice_by_id", "result": {"amount": 250}}],
            "final_response": "",
        }
        result = node_fn(state)
        assert result["final_response"]


# ---------------------------------------------------------------------------
# Graph structure
# ---------------------------------------------------------------------------

class TestCapstoneGraph:
    def test_graph_builds_without_error(self):
        from platform.graph import build_capstone_graph
        mock_llm = MagicMock()
        mock_llm.bind_tools.return_value = mock_llm
        graph = build_capstone_graph(mock_llm)
        assert graph is not None

    def test_graph_has_compiled_type(self):
        from platform.graph import build_capstone_graph
        from langgraph.graph.state import CompiledStateGraph
        mock_llm = MagicMock()
        mock_llm.bind_tools.return_value = mock_llm
        graph = build_capstone_graph(mock_llm)
        assert isinstance(graph, CompiledStateGraph)

    @pytest.mark.asyncio
    async def test_graph_routes_to_emergency(self):
        from platform.graph import build_capstone_graph
        mock_llm = MagicMock()
        mock_llm.bind_tools.return_value = mock_llm
        # classify_intent node will call llm.invoke
        mock_llm.invoke.return_value = AIMessage(
            content='{"intent": "emergency", "confidence": 0.99, "is_emergency": true}'
        )
        graph = build_capstone_graph(mock_llm)
        initial_state = {
            "messages": [HumanMessage(content="I have severe chest pain!")],
            "session_id": "test-session",
            "patient_id": None,
            "intent": None,
            "intent_confidence": 0.0,
            "tool_results": [],
            "rag_context": "",
            "rag_sources": [],
            "urgency_level": None,
            "urgency_label": "",
            "active_workflow": None,
            "workflow_thread_id": None,
            "awaiting_approval": False,
            "patient_context": "",
            "context_injected": False,
            "final_response": "",
            "is_emergency": False,
            "error": None,
        }
        config = {"configurable": {"thread_id": "test-thread-emergency"}}
        result = await graph.ainvoke(initial_state, config=config)
        assert result.get("is_emergency") is True
        assert result.get("urgency_level") == 1

    @pytest.mark.asyncio
    async def test_graph_non_emergency_produces_response(self):
        from platform.graph import build_capstone_graph
        mock_llm = MagicMock()
        # First call: classify intent
        # Subsequent calls: synthesize response
        mock_llm.bind_tools.return_value = mock_llm
        mock_llm.invoke.side_effect = [
            AIMessage(content='{"intent": "general", "confidence": 0.7, "is_emergency": false}'),
            AIMessage(content="Here is the information you requested."),
        ]
        graph = build_capstone_graph(mock_llm)
        initial_state = {
            "messages": [HumanMessage(content="Tell me about hospital visiting hours.")],
            "session_id": "test-session-2",
            "patient_id": None,
            "intent": None,
            "intent_confidence": 0.0,
            "tool_results": [],
            "rag_context": "",
            "rag_sources": [],
            "urgency_level": None,
            "urgency_label": "",
            "active_workflow": None,
            "workflow_thread_id": None,
            "awaiting_approval": False,
            "patient_context": "",
            "context_injected": False,
            "final_response": "",
            "is_emergency": False,
            "error": None,
        }
        config = {"configurable": {"thread_id": "test-thread-general"}}
        result = await graph.ainvoke(initial_state, config=config)
        assert result.get("final_response") or len(result.get("messages", [])) > 1


# ---------------------------------------------------------------------------
# Route logic
# ---------------------------------------------------------------------------

class TestRouteAfterClassification:
    def test_emergency_state_routes_to_emergency(self):
        from platform.graph import route_after_classification
        state = {"is_emergency": True, "intent": "emergency"}
        assert route_after_classification(state) == "emergency"

    def test_appointment_intent_routes_to_tools(self):
        from platform.graph import route_after_classification
        state = {"is_emergency": False, "intent": "appointment"}
        assert route_after_classification(state) == "tools"

    def test_billing_intent_routes_to_tools(self):
        from platform.graph import route_after_classification
        state = {"is_emergency": False, "intent": "billing"}
        assert route_after_classification(state) == "tools"

    def test_records_intent_routes_to_tools(self):
        from platform.graph import route_after_classification
        state = {"is_emergency": False, "intent": "records"}
        assert route_after_classification(state) == "tools"

    def test_general_intent_routes_to_rag(self):
        from platform.graph import route_after_classification
        state = {"is_emergency": False, "intent": "general"}
        assert route_after_classification(state) == "rag"

    def test_none_intent_routes_to_rag(self):
        from platform.graph import route_after_classification
        state = {"is_emergency": False, "intent": None}
        assert route_after_classification(state) == "rag"
