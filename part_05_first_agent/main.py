"""Part 5 — FastAPI endpoint to invoke the triage agent."""

import uuid
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage

from part_05_first_agent.agent.graph import triage_graph, get_graph_mermaid
from shared.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Part 5 — Triage Agent app starting")
    yield


app = FastAPI(
    title="Hospital AI Platform — Part 5: First LangGraph Agent",
    description="Stateful triage agent with LangGraph.",
    version="1.0.0",
    lifespan=lifespan,
)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    session_id: str | None = None


class ChatResponse(BaseModel):
    session_id: str
    response: str
    urgency_level: int | None = None
    urgency_label: str | None = None
    intake_complete: bool = False
    analysis_complete: bool = False


@app.post("/triage/chat", response_model=ChatResponse)
async def triage_chat(request: ChatRequest) -> ChatResponse:
    """Chat with the triage agent. Creates or resumes a session."""
    session_id = request.session_id or str(uuid.uuid4())
    config = {"configurable": {"thread_id": session_id}}

    try:
        state = await triage_graph.ainvoke(
            {"messages": [HumanMessage(content=request.message)]},
            config=config,
        )

        last_message = state["messages"][-1]
        return ChatResponse(
            session_id=session_id,
            response=last_message.content,
            urgency_level=state.get("urgency_level"),
            urgency_label=state.get("urgency_label"),
            intake_complete=state.get("intake_complete", False),
            analysis_complete=state.get("analysis_complete", False),
        )
    except Exception as exc:
        logger.error(f"Triage agent error: {exc}")
        raise HTTPException(status_code=500, detail="Triage agent encountered an error")


@app.get("/triage/graph")
async def get_graph():
    """Return the Mermaid diagram of the triage agent graph."""
    return {"mermaid": get_graph_mermaid()}


@app.get("/health")
async def health():
    return {"status": "healthy", "part": 5, "agent": "triage"}
