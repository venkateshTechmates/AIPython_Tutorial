"""Part 12 — Application metrics counters using a simple in-process registry.

For production, swap this for Prometheus client or OpenTelemetry.
"""

import time
import threading
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class MetricSnapshot:
    name: str
    value: float
    labels: dict[str, str] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)


class MetricsRegistry:
    """Thread-safe in-process metrics registry."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._counters: dict[str, float] = defaultdict(float)
        self._gauges: dict[str, float] = {}
        self._histograms: dict[str, list[float]] = defaultdict(list)

    # ------------------------------------------------------------------
    # Counters (monotonically increasing)
    # ------------------------------------------------------------------

    def increment(self, name: str, amount: float = 1.0) -> None:
        with self._lock:
            self._counters[name] += amount

    def get_counter(self, name: str) -> float:
        return self._counters.get(name, 0.0)

    # ------------------------------------------------------------------
    # Gauges (can go up or down)
    # ------------------------------------------------------------------

    def set_gauge(self, name: str, value: float) -> None:
        with self._lock:
            self._gauges[name] = value

    def get_gauge(self, name: str) -> Optional[float]:
        return self._gauges.get(name)

    # ------------------------------------------------------------------
    # Histograms (distribution of values)
    # ------------------------------------------------------------------

    def observe(self, name: str, value: float) -> None:
        with self._lock:
            self._histograms[name].append(value)

    def get_histogram_summary(self, name: str) -> dict:
        data = self._histograms.get(name, [])
        if not data:
            return {"count": 0}
        sorted_data = sorted(data)
        n = len(sorted_data)
        return {
            "count": n,
            "min": sorted_data[0],
            "max": sorted_data[-1],
            "mean": sum(sorted_data) / n,
            "p50": sorted_data[int(n * 0.50)],
            "p95": sorted_data[int(n * 0.95)],
            "p99": sorted_data[int(n * 0.99)],
        }

    # ------------------------------------------------------------------
    # Snapshot
    # ------------------------------------------------------------------

    def snapshot(self) -> dict:
        return {
            "counters": dict(self._counters),
            "gauges": dict(self._gauges),
            "histograms": {
                name: self.get_histogram_summary(name)
                for name in self._histograms
            },
        }


# Module-level singleton
_registry = MetricsRegistry()


def get_registry() -> MetricsRegistry:
    return _registry


# ------------------
# Named metric helpers
# ------------------

def record_llm_call(model: str, latency_ms: float, tokens: int, success: bool) -> None:
    r = get_registry()
    r.increment("llm.calls.total")
    r.increment(f"llm.calls.{model}")
    r.increment("llm.tokens.total", tokens)
    r.observe("llm.latency_ms", latency_ms)
    if not success:
        r.increment("llm.calls.errors")


def record_tool_call(tool_name: str, latency_ms: float, success: bool) -> None:
    r = get_registry()
    r.increment("tools.calls.total")
    r.increment(f"tools.calls.{tool_name}")
    r.observe("tools.latency_ms", latency_ms)
    if not success:
        r.increment("tools.calls.errors")


def record_http_request(method: str, path: str, status_code: int, latency_ms: float) -> None:
    r = get_registry()
    r.increment("http.requests.total")
    r.increment(f"http.requests.{status_code // 100}xx")
    r.observe("http.latency_ms", latency_ms)
    if status_code >= 500:
        r.increment("http.errors.5xx")
    elif status_code >= 400:
        r.increment("http.errors.4xx")
