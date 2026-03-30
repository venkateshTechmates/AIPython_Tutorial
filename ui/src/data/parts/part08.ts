import type { PartData } from "../../types";

export const part08: PartData = {
  id: "08",
  title: "Memory & State Management",
  goal: "Add three-tier memory to the agent: in-session short-term, SQLite long-term facts, and FAISS semantic recall.",
  phase: 3,
  phaseLabel: "Multi-Agent Systems",
  folder: "part_08_memory_state",
  estimatedHours: 5,
  difficulty: "advanced",
  prerequisites: ["05", "06", "07"],
  unlocks: ["09"],
  whatYouBuild: [
    { label: "POST /memory/chat", description: "Chat with full memory-aware agent" },
    { label: "POST /memory/save", description: "Persist a patient memory fact" },
    { label: "GET /memory/{patient_id}", description: "Retrieve all memory for a patient" },
    { label: "POST /memory/summary", description: "Add semantic summary to vector memory" },
    { label: "GET /memory/{patient_id}/recall", description: "Semantic recall by query" },
    { label: "GET /sessions", description: "List active sessions with TTL" },
  ],
  mermaidDiagram: `
flowchart TD
  subgraph Memory Tiers
    A[Short-Term\\nInMemoryChatMessageHistory\\nper session_id]
    B[Long-Term\\nSQLite patient_memories table\\nkey-value by category]
    C[Semantic\\nFAISS vector index\\npatient summaries]
  end

  D[MemoryManager] --> A
  D --> B
  D --> C
  D -->|build_context_prompt| E[System Message]
  E --> F[LangGraph Agent]
  F -->|new messages| A
  `,
  concepts: [
    {
      id: "short-term-memory",
      title: "Short-Term In-Session Memory",
      explanation:
        "InMemoryChatMessageHistory stores the conversation for the current session. It's cheap, fast, and automatically cleared when the session ends.",
      code: {
        language: "python",
        filename: "memory/short_term.py",
        snippet: `from langchain_core.chat_history import InMemoryChatMessageHistory

_sessions: dict[str, InMemoryChatMessageHistory] = {}

def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in _sessions:
        _sessions[session_id] = InMemoryChatMessageHistory()
    return _sessions[session_id]

def get_recent_messages(session_id: str, k: int = 10):
    history = get_session_history(session_id)
    return history.messages[-k:]`,
      },
      glossaryTerms: ["Memory", "Session", "Chat History"],
    },
    {
      id: "long-term-memory",
      title: "Long-Term SQLite Memory",
      explanation:
        "Long-term memory stores persistent facts about patients (preferences, chronic conditions, allergies). Organised by category and patient_id.",
      code: {
        language: "python",
        filename: "memory/long_term.py",
        snippet: `import sqlite3
from pathlib import Path

DB_PATH = Path("long_term_memory.db")

def upsert_memory(
    patient_id: str,
    category: str,  # preferences | history | context
    key: str,
    value: object
) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT OR REPLACE INTO patient_memories
            (patient_id, category, key, value, updated_at)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (patient_id, category, key, str(value)))`,
      },
    },
    {
      id: "semantic-memory",
      title: "Semantic Vector Memory",
      explanation:
        "FAISS semantic memory stores patient summaries as embeddings. You can query 'what happened in previous visits' using similarity search.",
      code: {
        language: "python",
        filename: "memory/semantic.py",
        snippet: `from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

def add_patient_summary(patient_id: str, summary: str):
    docs = [Document(
        page_content=summary,
        metadata={"patient_id": patient_id}
    )]
    # Add to FAISS index
    index.add_documents(docs)

def search_patient_memories(patient_id: str, query: str, k=3):
    results = index.similarity_search(
        query,
        k=k,
        filter={"patient_id": patient_id}
    )
    return [r.page_content for r in results]`,
      },
      glossaryTerms: ["FAISS", "Semantic Memory", "Embedding"],
    },
  ],
  steps: [
    { number: 1, title: "Implement short-term memory", description: "InMemoryChatMessageHistory per session_id with TTL eviction." },
    { number: 2, title: "Implement long-term SQLite memory", description: "patient_memories table with UPSERT on (patient_id, category, key)." },
    { number: 3, title: "Implement FAISS semantic memory", description: "Add/search patient summaries with patient_id filter." },
    { number: 4, title: "Build MemoryManager", description: "Unified interface that builds context_prompt from all three tiers." },
    { number: 5, title: "Inject memory into agent graph", description: "inject_context node prepends MemoryManager context as system message." },
    { number: 6, title: "Build SessionStore with TTL", description: "Auto-evict sessions after 30 minutes of inactivity." },
  ],
  acceptanceCriteria: [
    { id: "ac1", text: "Agent remembers patient preferences within a session" },
    { id: "ac2", text: "Long-term facts persist across server restarts" },
    { id: "ac3", text: "Semantic recall retrieves relevant past summaries" },
    { id: "ac4", text: "Sessions expire after TTL and are cleaned up" },
  ],
  gotchas: [
    {
      error: "FAISS IndexFlatL2: vectors must be of same dimension",
      cause: "Different embedding models produce different vector sizes",
      fix: "Always use the same embeddings instance for adding and searching",
    },
  ],
  resources: [
    { title: "LangGraph Memory", url: "https://langchain-ai.github.io/langgraph/concepts/memory/" },
    { title: "FAISS Docs", url: "https://faiss.ai/index.html" },
  ],
};
