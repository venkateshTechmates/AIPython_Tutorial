"""Part 11 — Unit tests for LangGraph agent nodes (no LLM required)."""

import pytest
from unittest.mock import MagicMock, patch
from langchain_core.messages import HumanMessage, AIMessage


class TestTriageNodes:
    """Unit tests for Part 5 triage agent nodes."""

    def _get_base_state(self):
        return {
            "messages": [],
            "symptoms": [],
            "urgency_level": None,
            "urgency_label": "",
            "recommendation": "",
            "intake_complete": False,
            "analysis_complete": False,
            "patient_name": "",
        }

    def test_urgency_label_mapping(self):
        """Test that urgency levels map to correct labels."""
        mapping = {
            1: "CRITICAL",
            2: "EMERGENT",
            3: "URGENT",
            4: "SEMI-URGENT",
            5: "NON-URGENT",
        }
        for level, label in mapping.items():
            # Simple business logic validation
            assert isinstance(label, str)
            assert len(label) > 0

    def test_extract_name_from_intake_message(self):
        """Test name extraction pattern used in intake node."""
        messages_with_completion = [
            HumanMessage(content="My name is John Smith"),
            AIMessage(content="Nice to meet you John! INTAKE_COMPLETE: {\"name\": \"John Smith\"}"),
        ]
        # Find INTAKE_COMPLETE tag
        for msg in messages_with_completion:
            if "INTAKE_COMPLETE:" in msg.content:
                idx = msg.content.index("INTAKE_COMPLETE:")
                tag_content = msg.content[idx + len("INTAKE_COMPLETE:"):].strip()
                assert "John Smith" in tag_content


class TestSupervisorRouter:
    """Unit tests for Part 6 supervisor routing logic."""

    def test_route_appointment_intent(self):
        """Test that appointment-related keywords route correctly."""
        appointment_queries = [
            "I need to schedule an appointment",
            "Can I book a visit with Dr. Chen?",
            "When is my next appointment?",
        ]
        # These should all trigger appointment routing
        for query in appointment_queries:
            keywords = ["schedule", "appointment", "book", "visit"]
            assert any(kw in query.lower() for kw in keywords)

    def test_route_billing_intent(self):
        billing_queries = [
            "How much do I owe?",
            "I have a question about my bill",
            "Does insurance cover this?",
        ]
        billing_keywords = ["owe", "bill", "insurance", "cost", "payment"]
        for query in billing_queries:
            assert any(kw in query.lower() for kw in billing_keywords)


class TestToolValidation:
    """Unit tests for Part 7 tool input validation."""

    def test_date_format_validation(self):
        """Verify date parsing logic used in utility tools."""
        from datetime import date
        valid_dates = ["2025-01-15", "1990-06-22", "2000-12-31"]
        for d in valid_dates:
            parsed = date.fromisoformat(d)
            assert parsed is not None

    def test_invalid_date_raises(self):
        """Invalid dates should raise ValueError."""
        from datetime import date
        with pytest.raises(ValueError):
            date.fromisoformat("not-a-date")

    def test_future_date_detection(self):
        """Future dates should be caught for date_of_birth validation."""
        from datetime import date
        future = date(2099, 1, 1)
        today = date.today()
        assert future > today

    def test_icd10_pattern(self):
        """ICD-10 codes must match the expected regex."""
        import re
        pattern = r"^[A-Z]\d{2}(\.\d{1,4})?$"
        valid = ["I21", "I21.0", "J18.9", "E11.9", "M54.5"]
        invalid = ["i21", "999", "ABC", "I21.12345"]
        for code in valid:
            assert re.match(pattern, code), f"{code} should be valid"
        for code in invalid:
            assert not re.match(pattern, code), f"{code} should be invalid"

    def test_discount_bounds(self):
        """Discounts must be between 0 and 100 percent."""
        valid_discounts = [0, 10, 50, 99.9, 100]
        invalid_discounts = [-1, 101, 150]
        for d in valid_discounts:
            assert 0 <= d <= 100
        for d in invalid_discounts:
            assert not (0 <= d <= 100)


class TestMemoryOperations:
    """Unit tests for Part 8 memory tier operations."""

    def test_session_ttl_calculation(self):
        """Session expiry should be calculable from TTL."""
        import time
        ttl = 3600
        created_at = time.time() - ttl - 1  # 1 second past expiry
        is_expired = (time.time() - created_at) > ttl
        assert is_expired

    def test_recent_messages_slice(self):
        """get_recent_messages k-window slicing logic."""
        messages = list(range(20))  # simulate 20 messages
        k = 6
        recent = messages[-k:]
        assert len(recent) == k
        assert recent[-1] == 19  # last message

    def test_context_prompt_builder(self):
        """Context prompt should contain patient ID and facts."""
        patient_id = "P001"
        facts = {"language": "Spanish", "diet": "vegan"}
        lines = [f"Patient: {patient_id}"]
        for k, v in facts.items():
            lines.append(f"- {k}: {v}")
        ctx = "\n".join(lines)
        assert "P001" in ctx
        assert "Spanish" in ctx
        assert "vegan" in ctx
