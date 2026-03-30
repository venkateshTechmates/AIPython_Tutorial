"""Part 14 — Capstone: Full Hospital Intelligence Platform FastAPI application."""

import sys
import time
from contextlib import asynccontextmanager
from typing import Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage, AIMessageChunk
from pydantic import BaseModel
from starlette.exceptions import HTTPException as StarletteHTTPException

sys.path.append("..")

# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class ChatRequest(BaseModel):
    message: str
    patient_id: Optional[str] = None
    session_id: Optional[str] = None
    stream: bool = False


class ChatResponse(BaseModel):
    session_id: str
    patient_id: Optional[str]
    response: str
    intent: Optional[str]
    intent_confidence: float
    is_emergency: bool
    urgency_level: Optional[int]
    latency_ms: float


class PatientContextRequest(BaseModel):
    patient_id: str
    key: str
    value: object
    category: str = "preferences"


# ---------------------------------------------------------------------------
# App lifecycle
# ---------------------------------------------------------------------------

_platform_graph = None
_llm = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _platform_graph, _llm
    try:
        from langchain_openai import ChatOpenAI
        from platform.graph import build_capstone_graph
        _llm = ChatOpenAI(model="gpt-4o", temperature=0.2, streaming=True)
        _platform_graph = build_capstone_graph(_llm)
    except Exception as exc:
        print(f"Warning: Could not initialize platform graph — {exc}")
        _platform_graph = None
    yield


app = FastAPI(
    title="Hospital Intelligence Platform",
    description=(
        "Part 14 — Capstone: The fully integrated Hospital AI Platform combining "
        "RAG, tool-calling, multi-agent orchestration, memory, HITL workflows, "
        "streaming, observability, and production hardening."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Error handlers
# ---------------------------------------------------------------------------

@app.exception_handler(StarletteHTTPException)
async def http_err_handler(request: Request, exc):
    from fastapi.responses import JSONResponse
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})


@app.exception_handler(RequestValidationError)
async def validation_err_handler(request: Request, exc):
    from fastapi.responses import JSONResponse
    return JSONResponse(status_code=422, content={"error": "Validation error", "details": exc.errors()})


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/")
async def root():
    return {
        "platform": "Hospital Intelligence Platform",
        "version": "1.0.0",
        "parts_integrated": list(range(1, 14)),
        "capabilities": [
            "Intent classification & routing",
            "Emergency escalation",
            "Tool calling (13 hospital tools)",
            "RAG over hospital documents",
            "Multi-tier memory (short/long/semantic)",
            "Human-in-the-loop workflows",
            "Real-time SSE streaming",
            "LangSmith observability",
            "Production rate limiting",
        ],
        "endpoints": {
            "chat": "POST /platform/chat",
            "stream": "POST /platform/chat?stream=true",
            "memory": "POST /platform/memory",
            "health": "GET /health",
        },
    }


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "platform_ready": _platform_graph is not None,
        "version": "1.0.0",
    }


@app.post("/platform/chat")
async def platform_chat(request: ChatRequest):
    """The unified patient journey endpoint.

    Routes automatically to the right agent/tool/workflow based on intent.
    Optionally streams the response via Server-Sent Events.
    """
    if _platform_graph is None:
        raise HTTPException(status_code=503, detail="Platform not available — check OPENAI_API_KEY.")

    session_id = request.session_id or str(uuid4())
    config = {"configurable": {"thread_id": session_id}}

    initial_state = {
        "messages": [HumanMessage(content=request.message)],
        "session_id": session_id,
        "patient_id": request.patient_id,
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

    if request.stream:
        # SSE streaming response
        async def stream_gen():
            import json
            async for chunk in _platform_graph.astream(
                initial_state,
                config=config,
                stream_mode="messages",
            ):
                msg_chunk, metadata = chunk
                if isinstance(msg_chunk, AIMessageChunk) and msg_chunk.content:
                    payload = json.dumps({"event": "token", "data": {"token": msg_chunk.content}})
                    yield f"data: {payload}\n\n"
            yield f"data: {json.dumps({'event': 'stream_end'})}\n\n"

        return StreamingResponse(stream_gen(), media_type="text/event-stream")

    # Non-streaming
    start = time.time()
    result = await _platform_graph.ainvoke(initial_state, config=config)
    latency_ms = (time.time() - start) * 1000

    final_response = result.get("final_response", "")
    if not final_response:
        # Fallback: get last AI message content
        for msg in reversed(result.get("messages", [])):
            if msg.type == "ai" and msg.content:
                final_response = msg.content
                break

    return ChatResponse(
        session_id=session_id,
        patient_id=request.patient_id,
        response=final_response,
        intent=result.get("intent"),
        intent_confidence=result.get("intent_confidence", 0.0),
        is_emergency=result.get("is_emergency", False),
        urgency_level=result.get("urgency_level"),
        latency_ms=round(latency_ms, 1),
    )


@app.post("/platform/memory")
async def save_patient_memory(request: PatientContextRequest):
    """Persist a long-term patient memory fact."""
    try:
        sys.path.insert(0, "../part_08_memory_state")
        from memory.long_term import upsert_memory
        upsert_memory(request.patient_id, request.category, request.key, request.value)
        return {"status": "saved", "patient_id": request.patient_id, "key": request.key}
    except ImportError:
        raise HTTPException(
            status_code=501,
            detail="Memory module not available — ensure part_08 is installed.",
        )


@app.get("/platform/patient/{patient_id}/memory")
async def get_patient_memory(patient_id: str):
    """Retrieve all stored memory for a patient."""
    try:
        sys.path.insert(0, "../part_08_memory_state")
        from memory.long_term import get_memory
        return {"patient_id": patient_id, "memory": get_memory(patient_id)}
    except ImportError:
        raise HTTPException(status_code=501, detail="Memory module not available.")
