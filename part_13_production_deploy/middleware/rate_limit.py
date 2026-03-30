"""Part 13 — Production-ready FastAPI middleware: rate limiting, structured logging, error handling."""

import time
import threading
from collections import defaultdict
from typing import Callable

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


# ---------------------------------------------------------------------------
# Rate limiter (token bucket, in-process)
# ---------------------------------------------------------------------------

class TokenBucketRateLimiter:
    """Per-IP token bucket rate limiter.

    NOT suitable for multi-process deployments — use Redis for that.
    """

    def __init__(self, max_requests: int = 30, window_seconds: int = 60) -> None:
        self._max = max_requests
        self._window = window_seconds
        self._buckets: dict[str, list[float]] = defaultdict(list)
        self._lock = threading.Lock()

    def is_allowed(self, client_ip: str) -> tuple[bool, int]:
        """Returns (allowed, remaining_requests)."""
        now = time.time()
        cutoff = now - self._window

        with self._lock:
            # Remove expired timestamps
            self._buckets[client_ip] = [
                ts for ts in self._buckets[client_ip] if ts > cutoff
            ]
            count = len(self._buckets[client_ip])

            if count >= self._max:
                return False, 0

            self._buckets[client_ip].append(now)
            return True, self._max - count - 1


class RateLimitMiddleware(BaseHTTPMiddleware):
    """FastAPI middleware that enforces per-IP rate limits."""

    def __init__(self, app, max_requests: int = 30, window_seconds: int = 60) -> None:
        super().__init__(app)
        self._limiter = TokenBucketRateLimiter(max_requests, window_seconds)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Allow health checks through without rate limiting
        if request.url.path in ("/health", "/metrics", "/docs", "/openapi.json"):
            return await call_next(request)

        client_ip = request.client.host if request.client else "unknown"
        allowed, remaining = self._limiter.is_allowed(client_ip)

        if not allowed:
            return JSONResponse(
                status_code=429,
                content={"error": "Too many requests", "retry_after_seconds": 60},
                headers={"Retry-After": "60"},
            )

        response = await call_next(request)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        return response
