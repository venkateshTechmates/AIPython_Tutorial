import type { PartData } from "../../types";

export const part12: PartData = {
  id: "12",
  title: "Observability & Tracing",
  goal: "Add LangSmith distributed tracing and a Prometheus-compatible metrics registry to the agent platform.",
  phase: 4,
  phaseLabel: "Production Patterns",
  folder: "part_12_observability",
  estimatedHours: 3,
  difficulty: "intermediate",
  prerequisites: ["05", "06", "07"],
  unlocks: ["13"],
  whatYouBuild: [
    { label: "POST /observe/chat", description: "Chat with full LangSmith tracing" },
    { label: "GET /metrics", description: "Prometheus-format metrics snapshot" },
  ],
  mermaidDiagram: `
flowchart LR
  subgraph Application
    A[FastAPI] --> B[LangGraph Agent]
    B --> C[LLM Calls]
    B --> D[Tool Calls]
  end

  subgraph Observability
    A -->|HTTP middleware| E[MetricsRegistry]
    C -->|CallbackHandler| F[LangSmith]
    D -->|CallbackHandler| F
    E --> G[GET /metrics]
    F --> H[LangSmith Dashboard]
  end
  `,
  concepts: [
    {
      id: "langsmith-tracing",
      title: "LangSmith Tracing",
      explanation:
        "LangSmith traces every LLM call, tool invocation, and chain step. Set LANGCHAIN_TRACING_V2=true and LANGCHAIN_API_KEY to enable automatic tracing.",
      code: {
        language: "python",
        filename: "tracing/setup.py",
        snippet: `import os
from langchain_core.tracers.langchain import LangChainTracer

def configure_langsmith(project_name: str, enabled: bool = True):
    if not enabled:
        os.environ["LANGCHAIN_TRACING_V2"] = "false"
        return
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_PROJECT"] = project_name

def build_run_config(session_id: str, patient_id: str | None):
    return {
        "run_name": f"hospital-ai-{session_id[:8]}",
        "metadata": {
            "session_id": session_id,
            "patient_id": patient_id,
        },
        "callbacks": [LangChainTracer()],
    }`,
      },
      glossaryTerms: ["LangSmith", "Tracing", "Observability"],
    },
    {
      id: "metrics-registry",
      title: "Custom Metrics Registry",
      explanation:
        "A thread-safe MetricsRegistry tracks counters, gauges, and histograms (p50/p95/p99 latencies). Exposed via GET /metrics for Prometheus scraping.",
      code: {
        language: "python",
        filename: "monitoring/metrics.py",
        snippet: `import threading, time
from collections import defaultdict

class MetricsRegistry:
    def __init__(self):
        self._lock = threading.Lock()
        self._counters: dict[str, float] = defaultdict(float)
        self._histograms: dict[str, list[float]] = defaultdict(list)

    def increment(self, name: str, value: float = 1):
        with self._lock:
            self._counters[name] += value

    def observe(self, name: str, value: float):
        with self._lock:
            self._histograms[name].append(value)

    def snapshot(self) -> dict:
        with self._lock:
            return {
                "counters": dict(self._counters),
                "histograms": {
                    k: self._percentiles(v)
                    for k, v in self._histograms.items()
                }
            }`,
      },
    },
  ],
  steps: [
    { number: 1, title: "Configure LangSmith", description: "Set env vars and build_run_config() helper for run metadata." },
    { number: 2, title: "Add MetadataCallbackHandler", description: "Capture model, tokens, and latency per LLM call." },
    { number: 3, title: "Build MetricsRegistry", description: "Thread-safe counters and histogram with percentiles." },
    { number: 4, title: "Add HTTP middleware", description: "Track request count and latency per endpoint." },
    { number: 5, title: "Wire GET /metrics endpoint", description: "Return full snapshot in Prometheus exposition format." },
  ],
  acceptanceCriteria: [
    { id: "ac1", text: "LangSmith shows full trace for each /observe/chat call" },
    { id: "ac2", text: "GET /metrics returns llm_calls_total counter" },
    { id: "ac3", text: "p95 latency calculated correctly for 100+ observations" },
    { id: "ac4", text: "Metrics persist across requests (not reset on each call)" },
  ],
  gotchas: [
    {
      error: "LangSmith traces not appearing despite LANGCHAIN_TRACING_V2=true",
      cause: "LANGCHAIN_API_KEY not set or expired",
      fix: "Generate a fresh API key from smith.langchain.com and update .env",
    },
  ],
  resources: [
    { title: "LangSmith Docs", url: "https://docs.smith.langchain.com/" },
    { title: "Prometheus Data Model", url: "https://prometheus.io/docs/concepts/data_model/" },
  ],
};
