"""Part 6 — FastAPI app for multi-agent orchestration."""

import uuid
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage

from part_06_multi_agent.orchestrator.graph import multi_agent_graph
from shared.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Part 6 — Multi-Agent Orchestration app starting")
    yield


app = FastAPI(
    title="Hospital AI Platform — Part 6: Multi-Agent Orchestration",
    description="Supervisor + 4 specialized sub-agents.",
    version="1.0.0",
    lifespan=lifespan,
)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    session_id: str | None = None


class ChatResponse(BaseModel):
    session_id: str
    response: str
    intent: str | None = None
    agent_used: str | None = None


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """Route user message to the appropriate specialist agent."""
    session_id = request.session_id or str(uuid.uuid4())
    config = {"configurable": {"thread_id": session_id}}

    try:
        state = await multi_agent_graph.ainvoke(
            {"messages": [HumanMessage(content=request.message)]},
            config=config,
        )
        last_msg = state["messages"][-1]
        return ChatResponse(
            session_id=session_id,
            response=last_msg.content,
            intent=state.get("intent"),
            agent_used=state.get("agent_used"),
        )
    except Exception as exc:
        logger.error(f"Multi-agent error: {exc}")
        raise HTTPException(status_code=500, detail="Agent system encountered an error")


@app.get("/health")
async def health():
    return {"status": "healthy", "part": 6, "agents": ["appointment", "billing", "records", "triage"]}
