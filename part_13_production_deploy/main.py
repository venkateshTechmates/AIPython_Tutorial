"""Part 13 — Production-hardened FastAPI application."""

import sys
import os
from contextlib import asynccontextmanager
from typing import Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from langchain_core.messages import HumanMessage
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

sys.path.append("..")


# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------

class Settings(BaseSettings):
    environment: str = "development"
    debug: bool = False
    openai_api_key: str = ""
    llm_model: str = "gpt-4o"
    database_url: str = "sqlite+aiosqlite:///./data/hospital.db"
    qdrant_url: str = "http://localhost:6333"
    rate_limit_requests: int = 30
    rate_limit_window_seconds: int = 60
    allowed_origins: str = "*"
    workers: int = 1

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    session_id: str
    response: str
    environment: str


# ---------------------------------------------------------------------------
# App lifecycle
# ---------------------------------------------------------------------------

_agent = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _agent
    try:
        from langchain_openai import ChatOpenAI
        _agent = ChatOpenAI(model=settings.llm_model, temperature=0.1)
    except Exception:
        _agent = None
    yield


app = FastAPI(
    title="Hospital Intelligence Platform",
    description="Part 13 — Production deployment with rate limiting and error handling",
    version="0.13.0",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    lifespan=lifespan,
)

# ---------------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------------

from middleware.rate_limit import RateLimitMiddleware
from middleware.error_handler import (
    http_exception_handler,
    validation_exception_handler,
    unhandled_exception_handler,
)

app.add_middleware(
    RateLimitMiddleware,
    max_requests=settings.rate_limit_requests,
    window_seconds=settings.rate_limit_window_seconds,
)

origins = settings.allowed_origins.split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)

app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "environment": settings.environment,
        "agent_ready": _agent is not None,
        "version": "0.13.0",
    }


@app.get("/")
async def root():
    return {
        "part": 13,
        "title": "Production Deployment",
        "environment": settings.environment,
        "features": ["rate_limiting", "error_handling", "docker", "non_root_container"],
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if _agent is None:
        raise HTTPException(status_code=503, detail="Agent not available.")

    session_id = request.session_id or str(uuid4())
    system = "You are a production Hospital AI Assistant. Be accurate, brief, and professional."

    response = _agent.invoke([
        {"role": "system", "content": system},
        HumanMessage(content=request.message),
    ])

    return ChatResponse(
        session_id=session_id,
        response=response.content,
        environment=settings.environment,
    )
