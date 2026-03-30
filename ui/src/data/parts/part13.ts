import type { PartData } from "../../types";

export const part13: PartData = {
  id: "13",
  title: "Production Deployment",
  goal: "Containerise the platform with Docker, add rate limiting, error handling, and a GitHub Actions CI/CD pipeline.",
  phase: 4,
  phaseLabel: "Production Patterns",
  folder: "part_13_production_deploy",
  estimatedHours: 4,
  difficulty: "advanced",
  prerequisites: ["01", "12"],
  unlocks: ["14"],
  whatYouBuild: [
    { label: "docker-compose up", description: "Run full stack with Docker Compose" },
    { label: "GET /health", description: "Production health check" },
    { label: "Nginx + 2 replicas", description: "Load-balanced production stack" },
  ],
  mermaidDiagram: `
flowchart TD
  subgraph Production Stack
    Nginx -->|proxy_pass| API1[API Replica 1]
    Nginx -->|proxy_pass| API2[API Replica 2]
    API1 --> Qdrant
    API2 --> Qdrant
  end

  subgraph Docker Compose
    A[api service\\nnon-root user\\nhealthcheck] 
    B[qdrant service\\npersistent volume]
    C[nginx service\\nSSL termination]
  end

  GitHub -->|push main| GHCI[GitHub Actions]
  GHCI -->|docker build| DockerHub
  DockerHub -->|deploy| Production Stack
  `,
  concepts: [
    {
      id: "dockerfile",
      title: "Production Dockerfile",
      explanation:
        "The production Dockerfile uses a non-root user, multi-stage build, and a pure-Python healthcheck to avoid installing curl in the image.",
      code: {
        language: "dockerfile",
        filename: "Dockerfile",
        snippet: `FROM python:3.11-slim

# Non-root user for security
RUN useradd -m -u 1000 appuser

WORKDIR /app
COPY --chown=appuser:appuser . .

RUN pip install uv && uv sync --frozen --no-dev

USER appuser
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s \\
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]`,
      },
      glossaryTerms: ["Docker", "Container", "Non-root User"],
    },
    {
      id: "rate-limiting",
      title: "Token Bucket Rate Limiting",
      explanation:
        "Token bucket rate limiting allows burst traffic up to a limit, then rejects requests with 429. Implemented as FastAPI middleware per IP address.",
      code: {
        language: "python",
        filename: "middleware/rate_limit.py",
        snippet: `import time, threading
from collections import defaultdict
from starlette.middleware.base import BaseHTTPMiddleware

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, requests_per_minute=60):
        super().__init__(app)
        self._window = 60
        self._limit = requests_per_minute
        self._buckets: dict[str, list[float]] = defaultdict(list)
        self._lock = threading.Lock()

    async def dispatch(self, request, call_next):
        ip = request.client.host
        now = time.time()
        with self._lock:
            bucket = self._buckets[ip]
            # Evict timestamps outside window
            self._buckets[ip] = [t for t in bucket if now - t < self._window]
            if len(self._buckets[ip]) >= self._limit:
                return Response("Rate limit exceeded", status_code=429)
            self._buckets[ip].append(now)
        return await call_next(request)`,
      },
      glossaryTerms: ["Rate Limiting", "Token Bucket", "Middleware"],
    },
  ],
  steps: [
    { number: 1, title: "Write the Dockerfile", description: "Multi-stage build, non-root user, uv, healthcheck." },
    { number: 2, title: "Create docker-compose.yml (dev)", description: "API + Qdrant services with healthchecks." },
    { number: 3, title: "Create docker-compose.prod.yml", description: "Add Nginx, 2 API replicas, resource limits." },
    { number: 4, title: "Implement rate limiting middleware", description: "Per-IP token bucket, returns 429 with Retry-After header." },
    { number: 5, title: "Add global error handlers", description: "Hide stack traces from clients, return structured error JSON." },
    { number: 6, title: "Test Docker build", description: "docker build -t hospital-ai . && docker run -e OPENAI_API_KEY=... -p 8000:8000 hospital-ai" },
  ],
  acceptanceCriteria: [
    { id: "ac1", text: "docker-compose up starts API and Qdrant successfully" },
    { id: "ac2", text: "API runs as non-root user inside container" },
    { id: "ac3", text: "Rate limiter returns 429 after 60 requests/minute" },
    { id: "ac4", text: "Unhandled exceptions return JSON {error:...} not raw traceback" },
    { id: "ac5", text: "Healthcheck endpoint passes inside container" },
  ],
  gotchas: [
    {
      error: "Permission denied: /app/hospital.db",
      cause: "Database file created before USER appuser switch",
      fix: "Create the db file after switching user, or set CHOWN on the data directory",
    },
    {
      error: "Connection refused: qdrant:6333",
      cause: "Service name in docker-compose.yml doesn't match the env var",
      fix: "Set QDRANT_URL=http://qdrant:6333 in the api service environment",
    },
  ],
  resources: [
    { title: "Docker Best Practices", url: "https://docs.docker.com/develop/develop-images/dockerfile_best-practices/" },
    { title: "FastAPI Deployment", url: "https://fastapi.tiangolo.com/deployment/" },
  ],
};
