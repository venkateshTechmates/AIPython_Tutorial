"""Part 10 — FastAPI streaming application with SSE and WebSocket endpoints."""

import sys
import json
from contextlib import asynccontextmanager
from typing import Optional
from uuid import uuid4

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, HTMLResponse
from langchain_core.messages import HumanMessage
from pydantic import BaseModel

sys.path.append("..")

from streaming.event_types import StreamEvent, StreamEventType
from streaming.stream_handler import stream_agent_response

# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    stream_mode: str = "events"  # "messages" | "events" | "updates"


# ---------------------------------------------------------------------------
# App lifecycle
# ---------------------------------------------------------------------------

_streaming_graph = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _streaming_graph
    try:
        from langchain_openai import ChatOpenAI
        from agent.streaming_agent import build_streaming_agent
        llm = ChatOpenAI(model="gpt-4o", temperature=0.3, streaming=True)
        _streaming_graph = build_streaming_agent(llm)
    except Exception:
        _streaming_graph = None
    yield


app = FastAPI(
    title="Hospital Streaming Agent",
    description="Part 10 — Real-time token streaming via SSE and WebSocket",
    version="0.10.0",
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
        "part": 10,
        "title": "Streaming & Real-Time Responses",
        "endpoints": {
            "sse_chat": "POST /stream/chat (Server-Sent Events)",
            "websocket_chat": "WS /stream/ws/{session_id}",
            "demo_ui": "GET /demo",
            "health": "GET /health",
        },
    }


@app.get("/health")
async def health():
    return {"status": "ok", "agent_ready": _streaming_graph is not None}


@app.post("/stream/chat")
async def stream_chat(request: ChatRequest):
    """Stream agent response via Server-Sent Events (SSE).

    The client should set ``Accept: text/event-stream`` and process the
    ``data: {...}\\n\\n`` events as they arrive.
    """
    if _streaming_graph is None:
        raise HTTPException(status_code=503, detail="Agent not available.")

    session_id = request.session_id or str(uuid4())

    async def generate():
        async for chunk in stream_agent_response(
            _streaming_graph,
            request.message,
            session_id,
            stream_mode=request.stream_mode,
        ):
            yield chunk

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Session-Id": session_id,
        },
    )


@app.websocket("/stream/ws/{session_id}")
async def websocket_chat(websocket: WebSocket, session_id: str):
    """WebSocket endpoint for bidirectional streaming conversation."""
    if _streaming_graph is None:
        await websocket.close(code=1011, reason="Agent not available")
        return

    await websocket.accept()
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            try:
                payload = json.loads(data)
                user_message = payload.get("message", data)
            except json.JSONDecodeError:
                user_message = data

            # Stream response back
            async for sse_chunk in stream_agent_response(
                _streaming_graph,
                user_message,
                session_id,
                stream_mode="events",
            ):
                # Strip the "data: " prefix and trailing newlines for WebSocket
                ws_payload = sse_chunk.replace("data: ", "").strip()
                await websocket.send_text(ws_payload)

    except WebSocketDisconnect:
        pass


@app.get("/demo", response_class=HTMLResponse)
async def demo_ui():
    """Simple HTML demo page for testing streaming in the browser."""
    return HTMLResponse(content=_DEMO_HTML)


_DEMO_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Hospital AI — Streaming Demo</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 800px; margin: 40px auto; padding: 0 20px; }
    h1 { color: #2c5282; }
    #chat { border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px; min-height: 300px;
            background: #f7fafc; overflow-y: auto; white-space: pre-wrap; font-size: 14px; }
    .controls { display: flex; gap: 8px; margin-top: 12px; }
    input { flex: 1; padding: 8px 12px; border: 1px solid #cbd5e0; border-radius: 6px; font-size: 14px; }
    button { padding: 8px 20px; background: #3182ce; color: white; border: none;
             border-radius: 6px; cursor: pointer; font-size: 14px; }
    button:hover { background: #2b6cb0; }
    .token { color: #1a202c; }
    .meta { color: #718096; font-style: italic; font-size: 12px; }
  </style>
</head>
<body>
  <h1>🏥 Hospital AI — Streaming Demo</h1>
  <div id="chat"><span class="meta">Streaming tokens will appear here in real-time...</span></div>
  <div class="controls">
    <input id="msg" type="text" placeholder="Ask a medical question..." value="What are the symptoms of hypertension?" />
    <button onclick="sendMessage()">Send (SSE)</button>
  </div>
  <script>
    async function sendMessage() {
      const input = document.getElementById('msg');
      const chat = document.getElementById('chat');
      const message = input.value.trim();
      if (!message) return;

      chat.innerHTML = `<span class="meta">You: ${message}\\n\\nAssistant: </span>`;
      input.value = '';

      const response = await fetch('/stream/chat', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ message, stream_mode: 'events' })
      });

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\\n\\n');
        buffer = lines.pop();

        for (const line of lines) {
          if (!line.startsWith('data:')) continue;
          try {
            const event = JSON.parse(line.slice(5).trim());
            if (event.event === 'token') {
              chat.innerHTML += `<span class="token">${event.data.token}</span>`;
              chat.scrollTop = chat.scrollHeight;
            } else if (event.event === 'tool_start') {
              chat.innerHTML += `\\n<span class="meta">[Tool: ${event.data.tool_name}]</span>\\n`;
            } else if (event.event === 'stream_end') {
              chat.innerHTML += `\\n<span class="meta">--- complete ---</span>`;
            }
          } catch(e) {}
        }
      }
    }

    document.getElementById('msg').addEventListener('keydown', e => {
      if (e.key === 'Enter') sendMessage();
    });
  </script>
</body>
</html>"""
