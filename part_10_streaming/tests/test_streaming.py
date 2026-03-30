"""Part 10 — Tests for streaming event types and stream handler."""

import pytest
import json
from unittest.mock import MagicMock, AsyncMock, patch


class TestStreamEventTypes:
    def test_stream_event_to_sse(self):
        from streaming.event_types import StreamEvent, StreamEventType
        event = StreamEvent(event=StreamEventType.TOKEN, data={"token": "Hello"})
        sse = event.to_sse()
        assert sse.startswith("data: ")
        assert sse.endswith("\n\n")

    def test_sse_payload_is_valid_json(self):
        from streaming.event_types import StreamEvent, StreamEventType
        event = StreamEvent(event=StreamEventType.TOOL_START, data={"tool": "lookup"}, run_id="r1")
        sse = event.to_sse()
        payload = json.loads(sse.replace("data: ", "").strip())
        assert payload["event"] == "tool_start"
        assert payload["run_id"] == "r1"

    def test_all_event_types_serialize(self):
        from streaming.event_types import StreamEvent, StreamEventType
        for et in StreamEventType:
            event = StreamEvent(event=et, data={"test": True})
            sse = event.to_sse()
            assert "data:" in sse


class TestStreamHandler:
    @pytest.mark.asyncio
    async def test_stream_emits_start_and_end(self):
        from streaming.stream_handler import stream_agent_response
        from streaming.event_types import StreamEventType

        # Mock graph with async astream
        mock_chunk = (MagicMock(content=""), {"run_id": "r1"})
        async def mock_astream(*args, **kwargs):
            yield mock_chunk

        mock_graph = MagicMock()
        mock_graph.astream = mock_astream

        events = []
        async for chunk in stream_agent_response(mock_graph, "Hello", "sess-1", "messages"):
            events.append(json.loads(chunk.replace("data: ", "").strip()))

        event_types = [e["event"] for e in events]
        assert "stream_start" in event_types
        assert "stream_end" in event_types

    @pytest.mark.asyncio
    async def test_stream_emits_tokens(self):
        from streaming.stream_handler import stream_agent_response
        from langchain_core.messages import AIMessageChunk

        token_chunk = AIMessageChunk(content="Hello")
        async def mock_astream(*args, **kwargs):
            yield (token_chunk, {"run_id": "r1"})

        mock_graph = MagicMock()
        mock_graph.astream = mock_astream

        events = []
        async for chunk in stream_agent_response(mock_graph, "Hi", "sess-2", "messages"):
            events.append(json.loads(chunk.replace("data: ", "").strip()))

        token_events = [e for e in events if e["event"] == "token"]
        assert len(token_events) == 1
        assert token_events[0]["data"]["token"] == "Hello"

    @pytest.mark.asyncio
    async def test_stream_handles_errors(self):
        from streaming.stream_handler import stream_agent_response

        async def mock_astream(*args, **kwargs):
            raise RuntimeError("Test error")
            yield  # pragma: no cover

        mock_graph = MagicMock()
        mock_graph.astream = mock_astream

        events = []
        async for chunk in stream_agent_response(mock_graph, "Crash", "sess-3", "events"):
            events.append(json.loads(chunk.replace("data: ", "").strip()))

        error_events = [e for e in events if e["event"] == "error"]
        assert len(error_events) >= 1
        assert "Test error" in error_events[0]["data"]["error"]
