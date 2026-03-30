import type { PartData } from "../../types";

export const part10: PartData = {
  id: "10",
  title: "Streaming Responses",
  goal: "Stream LLM tokens in real-time to the client using Server-Sent Events and WebSocket.",
  phase: 4,
  phaseLabel: "Production Patterns",
  folder: "part_10_streaming",
  estimatedHours: 3,
  difficulty: "intermediate",
  prerequisites: ["05", "06", "07"],
  unlocks: ["11"],
  whatYouBuild: [
    { label: "POST /stream/chat", description: "Chat with real-time SSE token streaming" },
    { label: "WS /stream/ws/{session_id}", description: "WebSocket streaming endpoint" },
    { label: "GET /demo", description: "Interactive HTML streaming demo page" },
  ],
  mermaidDiagram: `
sequenceDiagram
  participant Client
  participant FastAPI
  participant LangGraph
  participant OpenAI

  Client->>FastAPI: POST /stream/chat
  FastAPI->>LangGraph: astream(messages, stream_mode="messages")
  LangGraph->>OpenAI: streaming request

  loop Token by token
    OpenAI-->>LangGraph: AIMessageChunk
    LangGraph-->>FastAPI: (chunk, metadata)
    FastAPI-->>Client: data: {"event":"token","data":"Hello"}\n\n
  end

  FastAPI-->>Client: data: {"event":"stream_end"}\n\n
  `,
  concepts: [
    {
      id: "sse-format",
      title: "Server-Sent Events (SSE)",
      explanation:
        "SSE is a simple one-way HTTP streaming protocol. Each event is a line starting with 'data: ' followed by the payload. The connection stays open until the server closes it.",
      code: {
        language: "python",
        filename: "streaming/event_types.py",
        snippet: `from enum import Enum
import json

class StreamEventType(str, Enum):
    TOKEN = "token"
    TOOL_START = "tool_start"
    TOOL_END = "tool_end"
    ERROR = "error"
    STREAM_END = "stream_end"

def to_sse(event_type: StreamEventType, data: dict) -> str:
    payload = json.dumps({"event": event_type.value, "data": data})
    return f"data: {payload}\\n\\n"`,
      },
      glossaryTerms: ["SSE", "Streaming", "Server-Sent Events"],
    },
    {
      id: "streaming-response",
      title: "FastAPI StreamingResponse",
      explanation:
        "FastAPI wraps an async generator in StreamingResponse with media_type='text/event-stream'. The generator yields SSE formatted strings.",
      code: {
        language: "python",
        filename: "main.py",
        snippet: `from fastapi.responses import StreamingResponse
from langchain_core.messages import AIMessageChunk

@app.post("/stream/chat")
async def stream_chat(req: ChatRequest):
    async def generate():
        async for chunk, _ in graph.astream(
            {"messages": [HumanMessage(req.message)]},
            stream_mode="messages"
        ):
            if isinstance(chunk, AIMessageChunk) and chunk.content:
                yield to_sse(StreamEventType.TOKEN,
                            {"token": chunk.content})
        yield to_sse(StreamEventType.STREAM_END, {})

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache",
                 "X-Accel-Buffering": "no"}
    )`,
      },
    },
    {
      id: "client-eventsource",
      title: "Client-Side EventSource",
      explanation:
        "The browser's native EventSource API connects to an SSE endpoint and fires onmessage events for each token.",
      code: {
        language: "typescript",
        filename: "streaming/client.ts",
        snippet: `async function streamChat(message: string, onToken: (t: string) => void) {
  const response = await fetch("/stream/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });

  const reader = response.body!.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    const lines = decoder.decode(value).split("\\n");
    for (const line of lines) {
      if (line.startsWith("data: ")) {
        const event = JSON.parse(line.slice(6));
        if (event.event === "token") onToken(event.data.token);
      }
    }
  }
}`,
      },
      glossaryTerms: ["SSE", "ReadableStream", "EventSource"],
    },
  ],
  steps: [
    { number: 1, title: "Define StreamEvent types", description: "Create StreamEventType enum and to_sse() serialiser." },
    { number: 2, title: "Build the stream handler", description: "Async generator that wraps graph.astream() and yields SSE strings." },
    { number: 3, title: "Wire POST /stream/chat", description: "Return StreamingResponse with text/event-stream content type." },
    { number: 4, title: "Add WebSocket endpoint", description: "Alternative WS /stream/ws/{session_id} for bidirectional communication." },
    { number: 5, title: "Build the HTML demo page", description: "Static GET /demo page with JavaScript EventSource client." },
  ],
  acceptanceCriteria: [
    { id: "ac1", text: "Tokens appear individually in the browser as they are generated" },
    { id: "ac2", text: "stream_end event fires after the last token" },
    { id: "ac3", text: "WebSocket endpoint streams tokens to connected clients" },
    { id: "ac4", text: "Streaming errors emit error event instead of crashing" },
  ],
  gotchas: [
    {
      error: "Tokens appear in batches, not one-by-one",
      cause: "nginx or a proxy is buffering the SSE response",
      fix: "Add X-Accel-Buffering: no header to disable nginx buffering",
    },
    {
      error: "EventSource: CORS error",
      cause: "FastAPI CORS middleware not allowing the UI origin",
      fix: "Add allow_origins=['*'] or the specific UI origin to CORSMiddleware",
    },
  ],
  resources: [
    { title: "MDN EventSource API", url: "https://developer.mozilla.org/en-US/docs/Web/API/EventSource" },
    { title: "FastAPI WebSockets", url: "https://fastapi.tiangolo.com/advanced/websockets/" },
  ],
};
