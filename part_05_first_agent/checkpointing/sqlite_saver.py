"""Part 5 — SQLite-backed checkpointer for agent state persistence."""

import sqlite3
from pathlib import Path
from langgraph.checkpoint.sqlite import SqliteSaver


def get_sqlite_checkpointer(db_path: str = "./triage_checkpoints.db") -> SqliteSaver:
    """
    Create a SqliteSaver checkpointer for persisting agent state across sessions.

    Usage:
        checkpointer = get_sqlite_checkpointer()
        graph = build_triage_graph(checkpointer=checkpointer)

        # First turn
        config = {"configurable": {"thread_id": "session-123"}}
        result = graph.invoke({"messages": [HumanMessage("I have chest pain")]}, config)

        # Resume same session
        result = graph.invoke({"messages": [HumanMessage("It started 2 hours ago")]}, config)
    """
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path, check_same_thread=False)
    return SqliteSaver(conn)
