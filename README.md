# Hospital AI Platform — Agentic AI Mastery Tutorial Series

> **A production-grade, end-to-end learning workspace for building Agentic AI systems with Python, FastAPI, LangChain, LangGraph, Qdrant, and React.**

---

## 🌐 Live Demo (GitHub Pages)

**[https://venkateshTechmates.github.io/AIPython_Tutorial/](https://venkateshTechmates.github.io/AIPython_Tutorial/)**

> The UI is automatically deployed to GitHub Pages from the `gh-pages` branch.

---

## Overview

This monorepo teaches Agentic AI, RAG, GenAI, Vector Databases, and production-grade LLM system design through the lens of a **Hospital Intelligent Operations Platform**. Each of the 14 parts is a standalone, runnable application that incrementally builds on the previous one. By the end, you will have built a production-ready multi-agent hospital AI system complete with tool-calling, memory, streaming, human-in-the-loop, observability, and Docker deployment.

### Why a Hospital Domain?
- Rich real-world complexity: patients, doctors, appointments, billing, triage, records
- Natural fit for multi-agent workflows: scheduling agent, diagnosis agent, billing agent
- Enables RAG over medical literature, policies, and patient history
- Forces production concerns: sensitive data handling, validation, error handling

---

## Learning Objectives

| # | Competency |
|---|------------|
| 1 | Build and deploy LLM-powered APIs using FastAPI + LangChain |
| 2 | Design multi-agent systems with LangGraph (nodes, edges, state machines) |
| 3 | Implement RAG pipelines with Qdrant vector DB |
| 4 | Model and validate complex domains with Pydantic v2 |
| 5 | Persist agent state, memory, and history in SQLite |
| 6 | Structure production Python projects (config, logging, error handling) |
| 7 | Write integration tests for AI agents |
| 8 | Deploy multi-agent systems with Docker + FastAPI |
| 9 | Implement streaming, tool-calling, and human-in-the-loop patterns |
| 10 | Build observable, traceable AI systems with LangSmith |

---

## Tech Stack

### Backend
| Layer | Technology | Version |
|-------|-----------|---------|
| Language | Python | 3.11+ |
| API Framework | FastAPI | 0.115+ |
| Data Validation | Pydantic v2 | 2.7+ |
| AI Orchestration | LangChain | 0.3+ |
| Agent Graphs | LangGraph | 0.2+ |
| LLM Providers | OpenAI GPT-4o / Anthropic Claude | Latest |
| Vector DB | Qdrant | 1.9+ |
| Relational DB | SQLite + SQLAlchemy | 2.0+ |
| Embeddings | OpenAI `text-embedding-3-small` | Latest |
| Observability | LangSmith | Latest |
| Package Manager | `uv` | Latest |

### Frontend (Interactive Companion UI)
| Layer | Technology | Version |
|-------|-----------|---------|
| Framework | React + TypeScript | 18 / 5.5 |
| Build Tool | Vite | 5.4+ |
| Styling | Tailwind CSS | 3.4+ |
| Animations | Framer Motion | 11+ |
| Charts | Recharts | 2.12+ |
| State Management | Zustand | 4.5+ |
| Code Highlighting | Shiki | 1.12+ |
| Diagrams | Mermaid | 10.9+ |
| Routing | React Router DOM | 6.26+ |

---

## Repository Structure

```
hospital-ai-platform/
├── .gitignore
├── pyproject.toml               # Shared Python dependencies (uv)
├── docker-compose.yml           # Qdrant + SQLite viewer services
├── README.md
├── Tutorial.md                  # Full PRD & part-by-part specification
├── UI.md                        # UI companion documentation
│
├── shared/                      # Shared utilities across all parts
│   ├── config.py                # Pydantic BaseSettings
│   ├── logger.py                # Structured logging (loguru)
│   ├── models/                  # Shared Pydantic domain models
│   └── database/                # SQLite base setup
│
├── part_01_foundations/         # FastAPI + LangChain basics
├── part_02_pydantic_domain/     # Domain modeling with Pydantic v2
├── part_03_sqlite_persistence/  # SQLite + SQLAlchemy ORM
├── part_04_rag_qdrant/          # RAG pipeline with Qdrant
├── part_05_first_agent/         # First LangGraph agent
├── part_06_multi_agent/         # Multi-agent orchestration
├── part_07_tool_calling/        # Custom tools & function calling
├── part_08_memory_state/        # Agent memory & session state
├── part_09_human_in_loop/       # Human-in-the-loop workflows
├── part_10_streaming/           # Streaming responses & SSE
├── part_11_testing/             # Testing agents & RAG pipelines
├── part_12_observability/       # LangSmith tracing & monitoring
├── part_13_production_deploy/   # Docker, env management, prod patterns
├── part_14_capstone/            # Full Hospital AI Platform integrated
│
└── ui/                          # React companion UI (GitHub Pages)
    ├── src/
    │   ├── pages/               # Overview, Setup, PartDetail, Playground…
    │   ├── components/          # Shell, UI primitives, charts, etc.
    │   ├── store/               # Zustand (theme, progress, history)
    │   └── hooks/               # useTheme, useProgress, useBackendStatus
    └── package.json
```

---

## Part-by-Part Guide

### Part 01 — Foundations: FastAPI + LangChain
**`part_01_foundations/`**

Build a FastAPI app that talks to an LLM. Learn async endpoints, LCEL, and prompt engineering.

- `GET /health` — health check
- `POST /ask` — send a question to GPT-4o
- `POST /summarize` — summarize patient notes via a prompt template
- `POST /classify` — classify medical query type

**Key concepts:** FastAPI lifespan, `ChatOpenAI`, `PromptTemplate`, LCEL, async/await

---

### Part 02 — Pydantic Domain Modeling
**`part_02_pydantic_domain/`**

Model the hospital domain with Pydantic v2: patients, doctors, appointments, billing. Covers validators, computed fields, discriminated unions, and serialization.

**Key concepts:** `BaseModel`, `field_validator`, `model_validator`, `@computed_field`, `Annotated` types

---

### Part 03 — SQLite Persistence
**`part_03_sqlite_persistence/`**

Add a SQLite database layer with SQLAlchemy 2.0 async ORM. Repository pattern with full CRUD for patients, doctors, and appointments.

**Key concepts:** `AsyncSession`, `DeclarativeBase`, repository pattern, Alembic migrations

---

### Part 04 — RAG with Qdrant
**`part_04_rag_qdrant/`**

Build a full Retrieval-Augmented Generation pipeline. Ingest medical documents into Qdrant, then answer questions grounded in the knowledge base.

Pipeline: `Loader → Chunker → Embedder → Qdrant` → `Retriever → LLM Chain`

**Key concepts:** `RecursiveCharacterTextSplitter`, `OpenAIEmbeddings`, `QdrantVectorStore`, LCEL RAG chain

---

### Part 05 — First LangGraph Agent
**`part_05_first_agent/`**

Build your first stateful agent with LangGraph. A hospital triage agent that routes patient queries, uses tools, and maintains conversation state with SQLite checkpointing.

**Key concepts:** `StateGraph`, nodes, edges, conditional routing, `SqliteSaver`

---

### Part 06 — Multi-Agent Orchestration
**`part_06_multi_agent/`**

Orchestrate multiple specialized agents (triage, appointment, billing, records) under a supervisor agent. Each sub-agent is a LangGraph graph; the supervisor routes based on intent.

**Key concepts:** supervisor pattern, agent-as-tool, shared state, `send()` API

---

### Part 07 — Tool Calling
**`part_07_tool_calling/`**

Build a ReAct agent with custom tools: appointment booking, patient lookup, billing queries, medical record retrieval, and utility tools. Full tool schema validation.

**Key concepts:** `@tool`, `ToolNode`, `bind_tools`, schema validation, tool error handling

---

### Part 08 — Memory & State
**`part_08_memory_state/`**

Add short-term (in-window), long-term (persistent), and semantic (vector-based) memory to an agent. Sessions preserve context across conversations.

**Key concepts:** `ConversationBufferWindowMemory`, long-term store, semantic similarity recall, session management

---

### Part 09 — Human-in-the-Loop
**`part_09_human_in_loop/`**

Add human approval workflows for high-stakes operations (prescriptions, surgical scheduling, billing disputes). The agent pauses, requests approval, then resumes.

**Key concepts:** `interrupt_before`, `interrupt_after`, `update_state`, approval channels

---

### Part 10 — Streaming
**`part_10_streaming/`**

Stream LLM tokens and agent step events to the client in real time using SSE (Server-Sent Events) and LangChain streaming callbacks.

**Key concepts:** `astream_events`, `StreamingResponse`, SSE, token-level streaming, step events

---

### Part 11 — Testing
**`part_11_testing/`**

Comprehensive test suite: unit tests for tools and agents, integration tests against real LLMs, RAG evaluation with RAGAS, and golden-dataset testing.

**Key concepts:** `pytest-asyncio`, `respx` mocking, RAGAS metrics, golden datasets

---

### Part 12 — Observability
**`part_12_observability/`**

Instrument every LLM call, agent run, and retrieval with LangSmith. Build custom dashboards, set up alerts, and trace multi-agent runs end-to-end.

**Key concepts:** LangSmith tracing, `RunTree`, custom evaluators, cost tracking

---

### Part 13 — Production Deployment
**`part_13_production_deploy/`**

Package the entire platform for production: multi-stage Docker builds, environment-specific configs, rate limiting, auth middleware, health checks, and Docker Compose orchestration.

**Key concepts:** multi-stage Dockerfile, `slowapi` rate limiting, security headers, prod vs dev configs

---

### Part 14 — Capstone: Full Platform
**`part_14_capstone/`**

Integrate all 13 parts into a single, cohesive Hospital AI Platform. A production-ready multi-agent system with persistent memory, streaming, observability, and a full React UI.

---

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (fast Python package manager) — `pip install uv`
- Node.js 18+ and npm
- Docker Desktop (for Qdrant and SQLite viewer)
- OpenAI API key (and optionally Anthropic API key)
- LangSmith API key (Parts 12+, free tier available)

---

## Getting Started

### 1. Clone & set up Python environment

```bash
git clone https://github.com/venkateshTechmates/AIPython_Tutorial.git
cd AIPython_Tutorial

# Create virtual environment and install all dependencies
uv venv
uv pip install -e ".[dev]"
```

### 2. Configure environment variables

```bash
cp .env.example .env
# Edit .env and add your API keys:
#   OPENAI_API_KEY=sk-...
#   ANTHROPIC_API_KEY=sk-ant-...   (optional)
#   LANGCHAIN_API_KEY=ls__...      (optional, for Parts 12+)
```

### 3. Start Docker services (Qdrant + SQLite viewer)

```bash
docker compose up -d

# Qdrant dashboard: http://localhost:6333/dashboard
# SQLite web viewer: http://localhost:8081
```

### 4. Run a part

```bash
# Example: Part 01
cd part_01_foundations
uvicorn main:app --reload --port 8000

# Example: Part 05 (agent demo)
cd part_05_first_agent
python run_demo.py
```

---

## Running the Companion UI Locally

```bash
cd ui
npm install
npm run dev
# Opens at http://localhost:5173/AIPython_Tutorial/
```

### Deploy the UI to GitHub Pages

```bash
cd ui
npm run deploy
```

This command runs `npm run build` then pushes the `dist/` folder to the `gh-pages` branch of your repository.  
Your live URL will be:

```
https://venkateshTechmates.github.io/AIPython_Tutorial/
```

> **First deploy steps:**
> 1. Push your code to GitHub: `git push origin main`
> 2. Run `npm run deploy` from the `ui/` directory
> 3. In your GitHub repo → **Settings → Pages**, set **Source** to the `gh-pages` branch, `/ (root)`
> 4. Wait ~60 seconds for GitHub to publish the site

To use a custom domain, add a `CNAME` file inside `ui/public/` containing your domain name.

---

## UI Features

The companion React UI (`ui/`) provides an interactive learning dashboard:

| Feature | Description |
|---------|-------------|
| **Overview** | Animated part cards with prerequisites, tech tags, and unlock system |
| **Setup Checklist** | Step-by-step environment setup with interactive checkboxes |
| **Part Detail** | Full concepts, file structure, step guide, and acceptance criteria |
| **Playground** | Live HTTP tester — send requests to your running backend |
| **Progress Tracker** | Visual progress chart with completion dates and overall percentage |
| **Glossary** | Searchable AI/ML term definitions |
| **Multi-color Themes** | 6 accent palettes: Indigo · Violet · Teal · Rose · Amber · Sky |
| **Dark / Light Mode** | Full dark and light mode support |

---

## Environment Variables Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | ✅ Yes | OpenAI API key for GPT-4o and embeddings |
| `ANTHROPIC_API_KEY` | Optional | Anthropic Claude API key |
| `LANGCHAIN_API_KEY` | Optional | LangSmith API key (Parts 12+) |
| `LANGCHAIN_TRACING_V2` | Optional | Set `true` to enable LangSmith tracing |
| `LANGCHAIN_PROJECT` | Optional | LangSmith project name |
| `QDRANT_URL` | Optional | Qdrant URL (default: `http://localhost:6333`) |
| `DATABASE_URL` | Optional | SQLite path (default: `sqlite+aiosqlite:///./hospital.db`) |
| `DEBUG` | Optional | Enable debug logging |

---

## Docker Services

| Service | Port | Description |
|---------|------|-------------|
| Qdrant | 6333 (HTTP), 6334 (gRPC) | Vector database for RAG (Parts 4+) |
| SQLite Web | 8081 | Browser-based SQLite viewer |

```bash
docker compose up -d        # Start all services
docker compose down         # Stop all services
docker compose logs -f      # Follow logs
```

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/my-improvement`
3. Commit your changes: `git commit -m "feat: add X"`
4. Push to your fork: `git push origin feat/my-improvement`
5. Open a Pull Request

Please follow the existing code style and add tests for new functionality.

---

## License

MIT License — see [LICENSE](LICENSE) for details.
