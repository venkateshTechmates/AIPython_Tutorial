"""Part 10 — Stream handler: async generator over LangGraph stream events."""

import json
from typing import AsyncIterator

from langchain_core.messages import AIMessageChunk, HumanMessage

from streaming.event_types import StreamEvent, StreamEventType


async def stream_agent_response(
    graph,
    user_message: str,
    session_id: str,
    stream_mode: str = "messages",  # "messages" | "events" | "updates"
) -> AsyncIterator[str]:
    """Stream a LangGraph agent's response as SSE-formatted strings.

    Yields SSE wire-format strings suitable for use with FastAPI's
    ``StreamingResponse``.
    """
    config = {"configurable": {"thread_id": session_id}}

    # Signal start
    start_event = StreamEvent(
        event=StreamEventType.STREAM_START,
        data={"session_id": session_id, "message": user_message},
    )
    yield start_event.to_sse()

    try:
        async for chunk in graph.astream(
            {"messages": [HumanMessage(content=user_message)]},
            config=config,
            stream_mode=stream_mode,
        ):
            if stream_mode == "messages":
                # chunk is (message_chunk, metadata) tuple
                msg_chunk, metadata = chunk
                if isinstance(msg_chunk, AIMessageChunk) and msg_chunk.content:
                    token_event = StreamEvent(
                        event=StreamEventType.TOKEN,
                        data={"token": msg_chunk.content},
                        run_id=metadata.get("run_id"),
                    )
                    yield token_event.to_sse()

            elif stream_mode == "updates":
                # chunk is dict of node_name → state_update
                for node_name, update in chunk.items():
                    node_event = StreamEvent(
                        event=StreamEventType.NODE_END,
                        data={"node": node_name, "update_keys": list(update.keys()) if isinstance(update, dict) else []},
                    )
                    yield node_event.to_sse()

            elif stream_mode == "events":
                # chunk is a LangChain callback event dict
                event_name = chunk.get("event", "")
                if event_name == "on_chat_model_stream":
                    token = chunk.get("data", {}).get("chunk", {})
                    content = getattr(token, "content", "")
                    if content:
                        yield StreamEvent(
                            event=StreamEventType.TOKEN,
                            data={"token": content},
                            run_id=chunk.get("run_id"),
                        ).to_sse()
                elif event_name == "on_tool_start":
                    yield StreamEvent(
                        event=StreamEventType.TOOL_START,
                        data={
                            "tool_name": chunk.get("name", ""),
                            "tool_input": chunk.get("data", {}).get("input", {}),
                        },
                        run_id=chunk.get("run_id"),
                    ).to_sse()
                elif event_name == "on_tool_end":
                    yield StreamEvent(
                        event=StreamEventType.TOOL_END,
                        data={
                            "tool_name": chunk.get("name", ""),
                            "tool_output": str(chunk.get("data", {}).get("output", "")),
                        },
                        run_id=chunk.get("run_id"),
                    ).to_sse()

    except Exception as exc:
        yield StreamEvent(
            event=StreamEventType.ERROR,
            data={"error": str(exc)},
        ).to_sse()

    finally:
        yield StreamEvent(
            event=StreamEventType.STREAM_END,
            data={"session_id": session_id},
        ).to_sse()
