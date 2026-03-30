"""Part 12 — FastAPI observability application.

Demonstrates:
- LangSmith tracing configuration
- Request-scoped metadata injection
- In-process metrics collection
- /metrics endpoint for scraping
- Middleware for automatic HTTP instrumentation
"""

import sys
import time
from contextlib import asynccontextmanager
from typing import Optional
from uuid import uuid4

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from langchain_core.messages import HumanMessage
from pydantic import BaseModel

sys.path.append("..")

from tracing.setup import configure_langsmith
from tracing.metadata import build_run_config
from monitoring.metrics import (
    get_registry,
    record_http_request,
    record_llm_call,
)


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    patient_id: Optional[str] = None
    workflow: str = "general"


# ---------------------------------------------------------------------------
# App lifecycle
# ---------------------------------------------------------------------------

_agent = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _agent
    configure_langsmith()
    try:
        from langchain_openai import ChatOpenAI
        from langchain_core.messages import SystemMessage

        llm = ChatOpenAI(model="gpt-4o", temperature=0)
        _agent = llm
    except Exception:
        _agent = None
    yield


app = FastAPI(
    title="Hospital Observability Platform",
    description="Part 12 — LangSmith tracing, metrics, and monitoring",
    version="0.12.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# HTTP instrumentation middleware
# ---------------------------------------------------------------------------

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    latency_ms = (time.time() - start) * 1000
    record_http_request(
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        latency_ms=latency_ms,
    )
    response.headers["X-Response-Time-Ms"] = f"{latency_ms:.1f}"
    return response


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/")
async def root():
    return {
        "part": 12,
        "title": "Production Observability",
        "features": ["langsmith_tracing", "request_metadata", "in_process_metrics"],
        "endpoints": {
            "chat": "POST /observe/chat",
            "metrics": "GET /metrics",
            "health": "GET /health",
        },
    }


@app.get("/health")
async def health():
    r = get_registry()
    return {
        "status": "ok",
        "agent_ready": _agent is not None,
        "total_requests": r.get_counter("http.requests.total"),
        "total_llm_calls": r.get_counter("llm.calls.total"),
        "llm_errors": r.get_counter("llm.calls.errors"),
    }


@app.get("/metrics")
async def metrics():
    """Return a snapshot of all in-process metrics."""
    return get_registry().snapshot()


@app.post("/observe/chat")
async def observed_chat(request: ChatRequest):
    """Chat endpoint with full observability: tracing + metrics."""
    if _agent is None:
        raise HTTPException(status_code=503, detail="Agent not available.")

    session_id = request.session_id or str(uuid4())
    run_config = build_run_config(
        session_id=session_id,
        patient_id=request.patient_id,
        workflow=request.workflow,
        tags=["hospital", "chat", request.workflow],
    )

    llm_start = time.time()
    success = True
    tokens_used = 0

    try:
        system = "You are a Hospital AI Assistant. Be concise and professional."
        response = _agent.invoke(
            [
                {"role": "system", "content": system},
                HumanMessage(content=request.message),
            ],
            config=run_config,
        )
        latency_ms = (time.time() - llm_start) * 1000

        # Attempt to extract token usage (available when not streaming)
        usage = getattr(response, "usage_metadata", None)
        if usage:
            tokens_used = usage.get("total_tokens", 0)

        record_llm_call("gpt-4o", latency_ms, tokens_used, success=True)

        return {
            "session_id": session_id,
            "response": response.content,
            "workflow": request.workflow,
            "latency_ms": round(latency_ms, 1),
            "tokens_used": tokens_used,
        }

    except Exception as exc:
        latency_ms = (time.time() - llm_start) * 1000
        record_llm_call("gpt-4o", latency_ms, 0, success=False)
        raise HTTPException(status_code=500, detail=str(exc)) from exc
