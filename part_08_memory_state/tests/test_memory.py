"""Part 8 — Tests for all memory tiers and session store."""

import pytest
import time
from unittest.mock import patch


# ---------------------------------------------------------------------------
# Short-term memory
# ---------------------------------------------------------------------------

class TestShortTermMemory:
    def test_create_and_retrieve_session(self):
        from memory.short_term import add_user_message, add_ai_message, get_messages
        sid = "test-short-001"
        add_user_message(sid, "Hello")
        add_ai_message(sid, "Hi there!")
        msgs = get_messages(sid)
        assert len(msgs) == 2
        assert msgs[0].content == "Hello"
        assert msgs[1].content == "Hi there!"

    def test_get_recent_messages_truncates(self):
        from memory.short_term import add_user_message, add_ai_message, get_recent_messages
        sid = "test-short-002"
        for i in range(10):
            add_user_message(sid, f"msg {i}")
            add_ai_message(sid, f"reply {i}")
        recent = get_recent_messages(sid, k=4)
        assert len(recent) == 4

    def test_clear_session(self):
        from memory.short_term import add_user_message, clear_session, get_messages
        sid = "test-short-003"
        add_user_message(sid, "Something")
        clear_session(sid)
        assert len(get_messages(sid)) == 0

    def test_list_active_sessions(self):
        from memory.short_term import add_user_message, list_active_sessions
        sid = "test-short-004-unique"
        add_user_message(sid, "ping")
        sessions = list_active_sessions()
        assert sid in sessions


# ---------------------------------------------------------------------------
# Long-term memory
# ---------------------------------------------------------------------------

class TestLongTermMemory:
    def setup_method(self):
        # Use a temp DB path for tests
        import memory.long_term as lt_mod
        from pathlib import Path
        self._orig_path = lt_mod.DB_PATH
        lt_mod.DB_PATH = Path(__file__).parent.parent / "data" / "test_memory.db"
        lt_mod.DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    def teardown_method(self):
        import memory.long_term as lt_mod
        # Clean up test DB
        if lt_mod.DB_PATH.exists():
            lt_mod.DB_PATH.unlink()
        lt_mod.DB_PATH = self._orig_path

    def test_upsert_and_retrieve(self):
        from memory.long_term import upsert_memory, get_memory
        upsert_memory("P001", "preferences", "language", "Spanish")
        mem = get_memory("P001", "preferences")
        assert mem["preferences"]["language"] == "Spanish"

    def test_upsert_overwrites(self):
        from memory.long_term import upsert_memory, get_memory
        upsert_memory("P002", "context", "primary_doctor", "Dr. Smith")
        upsert_memory("P002", "context", "primary_doctor", "Dr. Jones")
        mem = get_memory("P002", "context")
        assert mem["context"]["primary_doctor"] == "Dr. Jones"

    def test_get_all_categories(self):
        from memory.long_term import upsert_memory, get_memory
        upsert_memory("P003", "preferences", "diet", "vegan")
        upsert_memory("P003", "history", "allergies", ["penicillin"])
        mem = get_memory("P003")
        assert "preferences" in mem
        assert "history" in mem

    def test_delete_specific_key(self):
        from memory.long_term import upsert_memory, get_memory, delete_memory
        upsert_memory("P004", "preferences", "language", "French")
        deleted = delete_memory("P004", "preferences", "language")
        assert deleted == 1
        mem = get_memory("P004", "preferences")
        assert "language" not in mem.get("preferences", {})

    def test_delete_entire_patient(self):
        from memory.long_term import upsert_memory, get_memory, delete_memory
        upsert_memory("P005", "history", "condition", "hypertension")
        upsert_memory("P005", "preferences", "language", "English")
        delete_memory("P005")
        assert get_memory("P005") == {}


# ---------------------------------------------------------------------------
# Session store
# ---------------------------------------------------------------------------

class TestSessionStore:
    def test_create_and_get(self):
        from sessions.session_store import SessionStore
        store = SessionStore()
        store.create("sess-1", "P001")
        s = store.get("sess-1")
        assert s is not None
        assert s.patient_id == "P001"

    def test_get_missing_returns_none(self):
        from sessions.session_store import SessionStore
        store = SessionStore()
        assert store.get("does-not-exist") is None

    def test_ttl_eviction(self):
        from sessions.session_store import SessionStore
        store = SessionStore(ttl_seconds=0)  # instant expiry
        store.create("sess-expired", "P002")
        time.sleep(0.01)
        result = store.get("sess-expired")
        assert result is None

    def test_update_metadata(self):
        from sessions.session_store import SessionStore
        store = SessionStore()
        store.create("sess-meta", "P003", metadata={"intent": "billing"})
        store.update_metadata("sess-meta", {"resolved": True})
        s = store.get("sess-meta")
        assert s.metadata["resolved"] is True
        assert s.metadata["intent"] == "billing"

    def test_delete(self):
        from sessions.session_store import SessionStore
        store = SessionStore()
        store.create("sess-del", "P004")
        assert store.delete("sess-del") is True
        assert store.get("sess-del") is None

    def test_count(self):
        from sessions.session_store import SessionStore
        store = SessionStore()
        store.create("sess-c1", "P005")
        store.create("sess-c2", "P006")
        assert store.count >= 2


# ---------------------------------------------------------------------------
# Memory manager
# ---------------------------------------------------------------------------

class TestMemoryManager:
    def setup_method(self):
        import memory.long_term as lt_mod
        from pathlib import Path
        self._orig_path = lt_mod.DB_PATH
        lt_mod.DB_PATH = Path(__file__).parent.parent / "data" / "test_mgr.db"
        lt_mod.DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    def teardown_method(self):
        import memory.long_term as lt_mod
        if lt_mod.DB_PATH.exists():
            lt_mod.DB_PATH.unlink()
        lt_mod.DB_PATH = self._orig_path

    def test_build_context_prompt(self):
        from memory.manager import MemoryManager
        mgr = MemoryManager(patient_id="PM001", session_id="sess-pm-001")
        mgr.save_preference("language", "Spanish")
        mgr.save_clinical_fact("allergies", ["penicillin", "sulfa"])
        mgr.remember_user_message("I feel dizzy")
        mgr.remember_ai_response("How long have you felt dizzy?")
        ctx = mgr.build_context_prompt()
        assert "PM001" in ctx
        assert "language" in ctx
        assert "Spanish" in ctx

    def test_forget_all(self):
        from memory.manager import MemoryManager
        mgr = MemoryManager(patient_id="PM002", session_id="sess-pm-002")
        mgr.save_preference("diet", "halal")
        deleted = mgr.forget()
        assert deleted >= 1
        assert mgr.get_patient_memory() == {}
