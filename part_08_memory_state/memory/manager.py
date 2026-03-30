"""Part 8 — Unified MemoryManager combining short-term, long-term, and semantic memory."""

from langchain_core.messages import BaseMessage

from memory.short_term import (
    add_user_message,
    add_ai_message,
    get_recent_messages,
    clear_session,
)
from memory.long_term import upsert_memory, get_memory, delete_memory
from memory.semantic import add_patient_summary, search_patient_memories


class MemoryManager:
    """High-level interface for all memory tiers.

    Usage::

        mgr = MemoryManager(patient_id="P001", session_id="sess-xyz")
        mgr.remember_user_message("I have chest pain")
        mgr.remember_ai_response("Please describe the pain in more detail.")
        context = mgr.build_context_prompt()
    """

    def __init__(self, patient_id: str, session_id: str) -> None:
        self.patient_id = patient_id
        self.session_id = session_id

    # ------------------------------------------------------------------
    # Short-term helpers
    # ------------------------------------------------------------------

    def remember_user_message(self, content: str) -> None:
        add_user_message(self.session_id, content)

    def remember_ai_response(self, content: str) -> None:
        add_ai_message(self.session_id, content)

    def get_conversation_history(self, k: int = 8) -> list[BaseMessage]:
        return get_recent_messages(self.session_id, k)

    def clear_conversation(self) -> None:
        clear_session(self.session_id)

    # ------------------------------------------------------------------
    # Long-term helpers
    # ------------------------------------------------------------------

    def save_preference(self, key: str, value: object) -> None:
        upsert_memory(self.patient_id, "preferences", key, value)

    def save_clinical_fact(self, key: str, value: object) -> None:
        upsert_memory(self.patient_id, "history", key, value)

    def save_context_fact(self, key: str, value: object) -> None:
        upsert_memory(self.patient_id, "context", key, value)

    def get_patient_memory(self, category: str | None = None) -> dict:
        return get_memory(self.patient_id, category)

    def forget(self, category: str | None = None, key: str | None = None) -> int:
        return delete_memory(self.patient_id, category, key)

    # ------------------------------------------------------------------
    # Semantic helpers
    # ------------------------------------------------------------------

    def save_clinical_summary(self, summary: str, metadata: dict | None = None) -> None:
        add_patient_summary(self.patient_id, summary, metadata)

    def recall_similar(self, query: str, k: int = 3) -> list[dict]:
        return search_patient_memories(query, patient_id=self.patient_id, k=k)

    # ------------------------------------------------------------------
    # Context assembly
    # ------------------------------------------------------------------

    def build_context_prompt(self) -> str:
        """Assemble a context block to prepend to the LLM system prompt."""
        lines = [f"## Patient Context (ID: {self.patient_id})"]

        long_term = self.get_patient_memory()
        if long_term:
            for category, facts in long_term.items():
                lines.append(f"\n### {category.title()}")
                for k, v in facts.items():
                    lines.append(f"- {k}: {v}")

        history = self.get_conversation_history(k=6)
        if history:
            lines.append("\n### Recent Conversation")
            for msg in history:
                role = "Patient" if msg.type == "human" else "Assistant"
                lines.append(f"- {role}: {msg.content[:200]}")

        return "\n".join(lines)
