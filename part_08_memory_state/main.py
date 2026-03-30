"""Part 8 — FastAPI application for the memory-enabled agent."""

import sys
from contextlib import asynccontextmanager
from typing import Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.messages import HumanMessage
from pydantic import BaseModel

sys.path.append("..")


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class MemoryChatRequest(BaseModel):
    message: str
    patient_id: str
    session_id: Optional[str] = None


class MemoryChatResponse(BaseModel):
    session_id: str
    patient_id: str
    response: str


class SaveMemoryRequest(BaseModel):
    patient_id: str
    category: str  # preferences | history | context
    key: str
    value: object


class SaveSummaryRequest(BaseModel):
    patient_id: str
    summary: str
    metadata: Optional[dict] = None


# ---------------------------------------------------------------------------
# App lifecycle
# ---------------------------------------------------------------------------

_agent_graph = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _agent_graph
    try:
        from langchain_openai import ChatOpenAI
        from agent.memory_agent import build_memory_agent_graph
        llm = ChatOpenAI(model="gpt-4o", temperature=0.3)
        _agent_graph = build_memory_agent_graph(llm)
    except Exception:
        _agent_graph = None
    yield


app = FastAPI(
    title="Hospital Memory Agent",
    description="Part 8 — Multi-tier memory: short-term, long-term, semantic",
    version="0.8.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/")
async def root():
    return {
        "part": 8,
        "title": "Memory & State Management",
        "memory_tiers": ["short_term (in-memory)", "long_term (SQLite)", "semantic (FAISS)"],
        "endpoints": {
            "chat": "POST /memory/chat",
            "save_memory": "POST /memory/save",
            "get_memory": "GET /memory/{patient_id}",
            "save_summary": "POST /memory/summary",
            "recall": "GET /memory/{patient_id}/recall?query=...",
            "sessions": "GET /sessions",
            "health": "GET /health",
        },
    }


@app.get("/health")
async def health():
    return {"status": "ok", "agent_ready": _agent_graph is not None}


@app.post("/memory/chat", response_model=MemoryChatResponse)
async def memory_chat(request: MemoryChatRequest):
    """Chat with an agent that has full multi-tier memory of the patient."""
    if _agent_graph is None:
        raise HTTPException(status_code=503, detail="Agent not available.")

    session_id = request.session_id or str(uuid4())
    config = {"configurable": {"thread_id": session_id}}

    result = await _agent_graph.ainvoke(
        {
            "messages": [HumanMessage(content=request.message)],
            "patient_id": request.patient_id,
            "session_id": session_id,
            "context_injected": False,
        },
        config=config,
    )

    final_response = ""
    for msg in reversed(result["messages"]):
        if msg.type == "ai" and msg.content:
            final_response = msg.content
            break

    return MemoryChatResponse(
        session_id=session_id,
        patient_id=request.patient_id,
        response=final_response,
    )


@app.post("/memory/save")
async def save_memory(request: SaveMemoryRequest):
    """Persist a long-term fact for a patient."""
    from memory.long_term import upsert_memory
    upsert_memory(
        patient_id=request.patient_id,
        category=request.category,
        key=request.key,
        value=request.value,
    )
    return {"status": "saved", "patient_id": request.patient_id, "key": request.key}


@app.get("/memory/{patient_id}")
async def get_memory(patient_id: str, category: Optional[str] = None):
    """Retrieve all stored long-term memory for a patient."""
    from memory.long_term import get_memory as _get_memory
    return {"patient_id": patient_id, "memory": _get_memory(patient_id, category)}


@app.post("/memory/summary")
async def save_summary(request: SaveSummaryRequest):
    """Embed and store a clinical summary in semantic memory."""
    from memory.semantic import add_patient_summary
    add_patient_summary(request.patient_id, request.summary, request.metadata)
    return {"status": "stored", "patient_id": request.patient_id}


@app.get("/memory/{patient_id}/recall")
async def recall_memories(patient_id: str, query: str, k: int = 3):
    """Semantically search stored summaries for a patient."""
    from memory.semantic import search_patient_memories
    results = search_patient_memories(query, patient_id=patient_id, k=k)
    return {"patient_id": patient_id, "query": query, "results": results}


@app.get("/sessions")
async def list_sessions():
    """List active sessions in the session store."""
    from sessions.session_store import get_session_store
    store = get_session_store()
    return {"sessions": store.list_sessions(), "total": store.count}
