"""Part 7 — FastAPI application for the tool-calling agent."""

import sys
from contextlib import asynccontextmanager
from typing import Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.messages import HumanMessage, AIMessage
from pydantic import BaseModel

sys.path.append("..")  # allow shared/ imports when running from this directory

from agent.graph import build_tool_agent_graph


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None


class ToolCallSummary(BaseModel):
    tool_name: str
    tool_input: dict
    tool_output: str


class ChatResponse(BaseModel):
    session_id: str
    response: str
    tools_called: list[ToolCallSummary]
    message_count: int


# ---------------------------------------------------------------------------
# App lifecycle
# ---------------------------------------------------------------------------

_agent_graph = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _agent_graph
    try:
        from langchain_openai import ChatOpenAI
        llm = ChatOpenAI(model="gpt-4o", temperature=0)
    except Exception:
        # Fallback: allow running without a valid key (tools still importable)
        llm = None

    if llm:
        _agent_graph = build_tool_agent_graph(llm)
    yield


app = FastAPI(
    title="Hospital Tool-Calling Agent",
    description="Part 7 — LangGraph ReAct agent with 13 hospital tools",
    version="0.7.0",
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
        "part": 7,
        "title": "Tool Calling & Function Execution",
        "tools_available": 13,
        "endpoints": {
            "chat": "POST /agent/chat",
            "tools_list": "GET /tools",
            "health": "GET /health",
        },
    }


@app.get("/health")
async def health():
    return {"status": "ok", "agent_ready": _agent_graph is not None}


@app.get("/tools")
async def list_tools():
    """List all available tools and their descriptions."""
    from tools import ALL_TOOLS
    return {
        "tools": [
            {
                "name": t.name,
                "description": t.description,
                "args_schema": t.args_schema.model_json_schema() if t.args_schema else {},
            }
            for t in ALL_TOOLS
        ],
        "total": len(ALL_TOOLS),
    }


@app.post("/agent/chat", response_model=ChatResponse)
async def agent_chat(request: ChatRequest):
    """Chat with the hospital assistant. The agent will use tools as needed."""
    if _agent_graph is None:
        raise HTTPException(
            status_code=503,
            detail="Agent not available — check OPENAI_API_KEY environment variable.",
        )

    session_id = request.session_id or str(uuid4())
    config = {"configurable": {"thread_id": session_id}}

    result = await _agent_graph.ainvoke(
        {"messages": [HumanMessage(content=request.message)]},
        config=config,
    )

    messages = result["messages"]

    # Extract the final AI response (last AIMessage)
    final_response = ""
    for msg in reversed(messages):
        if isinstance(msg, AIMessage) and msg.content:
            final_response = msg.content
            break

    # Extract tool calls made during this turn
    tools_called: list[ToolCallSummary] = []
    for i, msg in enumerate(messages):
        if isinstance(msg, AIMessage) and msg.tool_calls:
            for tc in msg.tool_calls:
                # The next message(s) contain tool outputs
                output = ""
                # Tool outputs appear as ToolMessage in subsequent positions
                for follow_msg in messages[i + 1:]:
                    if hasattr(follow_msg, "tool_call_id") and follow_msg.tool_call_id == tc["id"]:
                        output = str(follow_msg.content)
                        break
                tools_called.append(
                    ToolCallSummary(
                        tool_name=tc["name"],
                        tool_input=tc["args"],
                        tool_output=output,
                    )
                )

    return ChatResponse(
        session_id=session_id,
        response=final_response,
        tools_called=tools_called,
        message_count=len(messages),
    )
