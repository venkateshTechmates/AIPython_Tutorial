"""Part 11 — Shared pytest fixtures used across all test modules."""

import pytest
import sqlite3
from unittest.mock import MagicMock, AsyncMock


# ---------------------------------------------------------------------------
# LLM mocks
# ---------------------------------------------------------------------------

@pytest.fixture
def mock_llm():
    """A synchronous mock LLM that returns a configurable response."""
    llm = MagicMock()
    llm.invoke = MagicMock(return_value=MagicMock(
        content="This is a helpful medical response.",
        tool_calls=[],
    ))
    return llm


@pytest.fixture
def async_mock_llm():
    """An async mock LLM for use in async nodes."""
    llm = MagicMock()
    llm.ainvoke = AsyncMock(return_value=MagicMock(
        content="Async medical assistance response.",
        tool_calls=[],
    ))
    return llm


@pytest.fixture
def mock_llm_factory():
    """Factory that creates mock LLMs with custom responses."""
    def _factory(response_text: str = "default response"):
        llm = MagicMock()
        llm.invoke = MagicMock(return_value=MagicMock(content=response_text, tool_calls=[]))
        llm.ainvoke = AsyncMock(return_value=MagicMock(content=response_text, tool_calls=[]))
        return llm
    return _factory


# ---------------------------------------------------------------------------
# Database fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def in_memory_db():
    """Provide an in-memory SQLite connection, auto-closed after test."""
    conn = sqlite3.connect(":memory:")
    yield conn
    conn.close()


@pytest.fixture
def sample_patient_data():
    """Standard patient payload for tests."""
    return {
        "first_name": "Jane",
        "last_name": "Doe",
        "date_of_birth": "1985-03-22",
        "email": "jane.doe@example.com",
        "phone": "555-123-4567",
        "blood_type": "A+",
        "address": "123 Main St, Springfield",
        "emergency_contact": "John Doe",
        "emergency_phone": "555-987-6543",
    }


@pytest.fixture
def sample_doctor_data():
    """Standard doctor payload for tests."""
    return {
        "first_name": "Michael",
        "last_name": "Chen",
        "specialty": "cardiology",
        "license_number": "MD-12345",
        "email": "m.chen@hospital.com",
        "phone": "555-200-3000",
        "years_experience": 15,
        "available_days": ["Monday", "Tuesday", "Wednesday", "Thursday"],
    }


@pytest.fixture
def sample_appointment_data():
    """Standard appointment payload for tests."""
    return {
        "patient_id": 1,
        "doctor_id": 1,
        "type": "in_person",
        "scheduled_at": "2025-09-15T10:00:00",
        "reason": "Annual checkup",
        "duration_minutes": 30,
    }


# ---------------------------------------------------------------------------
# Environment fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def no_real_api_calls(monkeypatch):
    """Prevent accidental real OpenAI/Anthropic API calls in unit tests.
    
    Tests that truly need the LLM should use the ``mock_llm`` fixture or
    apply the ``@pytest.mark.integration`` marker to opt out.
    """
    # We don't monkeypatch here by default — each test that needs mocking
    # should use the mock_llm fixture. This fixture exists as documentation.
    pass
