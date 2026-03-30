"""Part 8 — Short-term (within-session) conversation memory using LangChain."""

from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage

# session_id → InMemoryChatMessageHistory
_short_term_store: dict[str, InMemoryChatMessageHistory] = {}


def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    """Retrieve or create an InMemory chat history for a given session."""
    if session_id not in _short_term_store:
        _short_term_store[session_id] = InMemoryChatMessageHistory()
    return _short_term_store[session_id]


def add_user_message(session_id: str, content: str) -> None:
    """Append a human message to the session history."""
    get_session_history(session_id).add_user_message(content)


def add_ai_message(session_id: str, content: str) -> None:
    """Append an AI message to the session history."""
    get_session_history(session_id).add_ai_message(content)


def get_messages(session_id: str) -> list[BaseMessage]:
    """Return all messages for a session."""
    return get_session_history(session_id).messages


def clear_session(session_id: str) -> None:
    """Clear all messages for a session."""
    if session_id in _short_term_store:
        _short_term_store[session_id].clear()


def get_recent_messages(session_id: str, k: int = 6) -> list[BaseMessage]:
    """Return the most recent *k* messages (k/2 exchanges), oldest first."""
    messages = get_messages(session_id)
    return messages[-k:] if len(messages) > k else messages


def list_active_sessions() -> list[str]:
    """Return all active session IDs."""
    return list(_short_term_store.keys())
