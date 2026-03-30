"""Part 8 — Long-term (persistent) patient memory stored in SQLite."""

import json
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "long_term_memory.db"


def _get_conn() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("""
        CREATE TABLE IF NOT EXISTS patient_memories (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id  TEXT    NOT NULL,
            category    TEXT    NOT NULL,
            key         TEXT    NOT NULL,
            value       TEXT    NOT NULL,
            created_at  TEXT    NOT NULL DEFAULT (datetime('now')),
            updated_at  TEXT    NOT NULL DEFAULT (datetime('now')),
            UNIQUE (patient_id, category, key)
        )
    """)
    conn.commit()
    return conn


def upsert_memory(patient_id: str, category: str, key: str, value: object) -> None:
    """Store or update a long-term memory fact for a patient.

    Categories:
        preferences   — care preferences, language, dietary restrictions
        history       — brief clinical history summaries
        context       — administrative context (payer, primary_doctor, etc.)
    """
    conn = _get_conn()
    now = datetime.utcnow().isoformat()
    conn.execute(
        """
        INSERT INTO patient_memories (patient_id, category, key, value, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(patient_id, category, key)
        DO UPDATE SET value=excluded.value, updated_at=excluded.updated_at
        """,
        (patient_id, category, key, json.dumps(value), now, now),
    )
    conn.commit()
    conn.close()


def get_memory(patient_id: str, category: str | None = None) -> dict:
    """Retrieve all stored facts for a patient, optionally filtered by category."""
    conn = _get_conn()
    if category:
        rows = conn.execute(
            "SELECT category, key, value FROM patient_memories WHERE patient_id = ? AND category = ?",
            (patient_id, category),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT category, key, value FROM patient_memories WHERE patient_id = ?",
            (patient_id,),
        ).fetchall()
    conn.close()

    result: dict[str, dict] = {}
    for row in rows:
        cat = row["category"]
        result.setdefault(cat, {})[row["key"]] = json.loads(row["value"])
    return result


def delete_memory(patient_id: str, category: str | None = None, key: str | None = None) -> int:
    """Delete memory entries. Returns number of rows deleted."""
    conn = _get_conn()
    if category and key:
        cur = conn.execute(
            "DELETE FROM patient_memories WHERE patient_id=? AND category=? AND key=?",
            (patient_id, category, key),
        )
    elif category:
        cur = conn.execute(
            "DELETE FROM patient_memories WHERE patient_id=? AND category=?",
            (patient_id, category),
        )
    else:
        cur = conn.execute("DELETE FROM patient_memories WHERE patient_id=?", (patient_id,))
    conn.commit()
    affected = cur.rowcount
    conn.close()
    return affected
