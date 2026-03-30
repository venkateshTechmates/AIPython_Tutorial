# 📋 Product Requirements Document
## Agentic AI Mastery — End-to-End Tutorial Series
### "Hospital Intelligence Platform" — A Production-Grade Learning Workspace

---

> **Version:** 1.0.0  
> **Status:** Draft  
> **Target Audience:** Mid–Senior Python Developers, AI/ML Engineers, Backend Engineers  
> **Delivery Format:** Mono-repo with progressive, runnable apps per part  

---

## 1. Vision & Purpose

Build a **single, cohesive monorepo** that teaches Agentic AI, RAG, GenAI, Vector Databases, and production-grade LLM system design — through the lens of a **Hospital Intelligent Operations Platform**. Each part is a standalone, runnable application that incrementally builds on the previous one. By the end of the series, learners will have built a production-ready multi-agent hospital AI system.

### Why a Hospital Domain?
- Rich, real-world complexity (patients, doctors, appointments, billing, triage, records)
- Natural fit for multi-agent workflows (scheduling agent, diagnosis agent, billing agent)
- Enables RAG over medical literature, policies, and patient history
- Forces learners to handle sensitive data, validation, error handling — production concerns

---

## 2. Learning Objectives

By completing all parts, learners will be able to:

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

## 3. Workspace Architecture

```
hospital-ai-platform/
│
├── README.md                        # Master guide & navigation
├── pyproject.toml                   # Shared dependencies (uv / poetry)
├── docker-compose.yml               # Qdrant, SQLite viewer, services
├── .env.example                     # All required env vars
├── shared/                          # Shared utilities across all parts
│   ├── models/                      # Pydantic domain models
│   ├── database/                    # SQLite base setup
│   ├── config.py                    # Settings (Pydantic BaseSettings)
│   └── logger.py                    # Structured logging
│
├── part_01_foundations/             # FastAPI + LangChain basics
├── part_02_pydantic_domain/         # Domain modeling with Pydantic v2
├── part_03_sqlite_persistence/      # SQLite + SQLAlchemy ORM
├── part_04_rag_qdrant/              # RAG pipeline with Qdrant
├── part_05_first_agent/             # First LangGraph agent
├── part_06_multi_agent/             # Multi-agent orchestration
├── part_07_tool_calling/            # Custom tools & function calling
├── part_08_memory_state/            # Agent memory & session state
├── part_09_human_in_loop/           # Human-in-the-loop workflows
├── part_10_streaming/               # Streaming responses & SSE
├── part_11_testing/                 # Testing agents & RAG pipelines
├── part_12_observability/           # LangSmith tracing & monitoring
├── part_13_production_deploy/       # Docker, env management, prod patterns
└── part_14_capstone/                # Full Hospital AI Platform integrated
```

---

## 4. Tech Stack

### Core
| Layer | Technology | Version |
|-------|-----------|---------|
| Language | Python | 3.11+ |
| API Framework | FastAPI | 0.115+ |
| Data Validation | Pydantic v2 | 2.7+ |
| AI Orchestration | LangChain | 0.3+ |
| Agent Graphs | LangGraph | 0.2+ |
| LLM Provider | OpenAI (GPT-4o) / Anthropic Claude | Latest |
| Vector DB | Qdrant | 1.9+ |
| Relational DB | SQLite + SQLAlchemy | 2.0+ |
| Embeddings | OpenAI `text-embedding-3-small` | Latest |
| Observability | LangSmith | Latest |

### Dev Tooling
| Tool | Purpose |
|------|---------|
| `uv` | Fast Python package manager |
| `pytest` + `pytest-asyncio` | Async test framework |
| `httpx` | Async HTTP client for testing FastAPI |
| `python-dotenv` | Environment management |
| `loguru` | Structured logging |
| `rich` | Console output for demos |
| Docker Compose | Local Qdrant + services |

---

## 5. Part-by-Part Specification

---

### PART 1 — Foundations: FastAPI + LangChain Hello World
**📁 `part_01_foundations/`**

**Goal:** Get a FastAPI app running that talks to an LLM. Understand request/response, async, basic prompt engineering.

**What You Build:**
- `GET /health` — basic health check
- `POST /ask` — send a question to GPT-4o, get answer
- `POST /summarize` — summarize patient notes using a prompt template
- `POST /classify` — classify medical query type (triage/billing/appointment)

**Key Concepts:**
- FastAPI app lifecycle (`lifespan`)
- LangChain `ChatOpenAI` / `ChatAnthropic`
- `PromptTemplate` and `ChatPromptTemplate`
- `LLMChain` → `LCEL` (LangChain Expression Language)
- Async endpoints with `async def`
- Pydantic request/response schemas

**File Structure:**
```
part_01_foundations/
├── main.py
├── routers/
│   ├── health.py
│   ├── ask.py
│   └── classify.py
├── schemas.py          # Request/Response Pydantic models
├── prompts.py          # All prompt templates
├── llm.py              # LLM factory
├── requirements.txt
└── README.md           # Step-by-step guide for this part
```

**Acceptance Criteria:**
- [ ] All 4 endpoints return correct responses
- [ ] LLM calls are async
- [ ] Prompts are externalized (not hardcoded in routes)
- [ ] `.env` based API key configuration

---

### PART 2 — Domain Modeling with Pydantic v2
**📁 `part_02_pydantic_domain/`**

**Goal:** Model the entire hospital domain with Pydantic v2. Learn validators, computed fields, discriminated unions, and nested models.

**What You Build:**
- Full domain model: `Patient`, `Doctor`, `Appointment`, `MedicalRecord`, `Prescription`, `Billing`
- Custom validators (e.g., date of birth validation, ICD code format)
- Serialization/deserialization to/from JSON and dict
- `model_config` with examples for FastAPI docs

**Key Concepts:**
- `BaseModel` vs `RootModel`
- `@field_validator`, `@model_validator`
- `computed_field`, `model_serializer`
- Discriminated unions (different appointment types)
- `ConfigDict` settings (frozen, populate_by_name, etc.)
- Pydantic Settings for configuration management

**File Structure:**
```
part_02_pydantic_domain/
├── models/
│   ├── patient.py
│   ├── doctor.py
│   ├── appointment.py
│   ├── medical_record.py
│   ├── prescription.py
│   └── billing.py
├── config.py           # Pydantic BaseSettings
├── validators.py       # Custom reusable validators
├── examples.py         # Usage demonstration
├── tests/
│   └── test_models.py
└── README.md
```

**Acceptance Criteria:**
- [ ] All domain models pass validation test suite
- [ ] Invalid data raises descriptive `ValidationError`
- [ ] Models serialize cleanly to JSON
- [ ] Settings load from `.env` file

---

### PART 3 — SQLite Persistence with SQLAlchemy 2.0
**📁 `part_03_sqlite_persistence/`**

**Goal:** Persist hospital data using SQLAlchemy 2.0 async ORM with SQLite. Build a clean repository pattern.

**What You Build:**
- Async SQLAlchemy models mapped to SQLite tables
- Repository classes for each entity (CRUD)
- Database migrations with Alembic
- FastAPI dependency injection for DB sessions
- Seed script with realistic hospital data

**Key Concepts:**
- `AsyncEngine`, `AsyncSession`, `async_sessionmaker`
- `DeclarativeBase` with typed columns
- SQLAlchemy 2.0 `select()` query style
- Repository Pattern (separation of DB logic from business logic)
- Alembic migration setup
- `Depends()` for DB session injection in FastAPI

**File Structure:**
```
part_03_sqlite_persistence/
├── database/
│   ├── base.py         # Engine, session factory
│   ├── models.py       # SQLAlchemy ORM models
│   └── migrations/     # Alembic migrations
├── repositories/
│   ├── patient_repo.py
│   ├── doctor_repo.py
│   └── appointment_repo.py
├── main.py             # FastAPI with DB-backed endpoints
├── dependencies.py     # FastAPI DB session dependency
├── seed.py             # Seed realistic test data
├── tests/
│   └── test_repositories.py
└── README.md
```

**Acceptance Criteria:**
- [ ] All CRUD operations work for Patient, Doctor, Appointment
- [ ] Async DB session is properly scoped per request
- [ ] Migrations run cleanly with Alembic
- [ ] Seed script populates 20+ patients, 10 doctors, 50 appointments

---

### PART 4 — RAG Pipeline with Qdrant Vector Database
**📁 `part_04_rag_qdrant/`**

**Goal:** Build a full Retrieval-Augmented Generation pipeline over hospital documents (medical policies, drug reference, clinical guidelines).

**What You Build:**
- Document ingestion pipeline (PDF/text → chunks → embeddings → Qdrant)
- Semantic search endpoint
- RAG Q&A endpoint: "What is the hospital's policy on medication dispensing?"
- Hybrid search (dense + sparse)
- Metadata filtering (search only within a department's documents)

**Key Concepts:**
- Qdrant collections, vectors, payload
- OpenAI `text-embedding-3-small` for embeddings
- LangChain `QdrantVectorStore`
- `RecursiveCharacterTextSplitter` chunking strategy
- `RetrievalQA` chain
- RAG prompt engineering (context injection)
- Qdrant filters with payload metadata

**File Structure:**
```
part_04_rag_qdrant/
├── ingestion/
│   ├── loader.py       # Document loaders (PDF, text, markdown)
│   ├── chunker.py      # Text splitting strategies
│   ├── embedder.py     # Embedding model wrapper
│   └── ingestor.py     # Full pipeline orchestrator
├── retrieval/
│   ├── qdrant_client.py
│   ├── retriever.py    # LangChain retriever wrapper
│   └── hybrid_search.py
├── rag/
│   ├── chain.py        # RAG chain with LCEL
│   └── prompts.py      # RAG system prompts
├── data/
│   └── documents/      # Sample hospital docs (PDFs, txt)
├── main.py             # FastAPI RAG endpoints
├── docker-compose.yml  # Qdrant container
├── ingest.py           # CLI ingestion script
├── tests/
│   └── test_rag.py
└── README.md
```

**Acceptance Criteria:**
- [ ] 50+ document chunks ingested into Qdrant
- [ ] Semantic search returns relevant results with scores
- [ ] RAG answers reference source documents
- [ ] Metadata filtering works (by department, doc type)
- [ ] Qdrant runs locally via Docker Compose

---

### PART 5 — First LangGraph Agent
**📁 `part_05_first_agent/`**

**Goal:** Build your first stateful agent with LangGraph. A hospital triage agent that collects patient symptoms and recommends urgency level.

**What You Build:**
- LangGraph `StateGraph` with typed state
- Triage agent: intake → symptom analysis → urgency classification → recommendation
- Conditional edges (low urgency vs. high urgency paths)
- Agent state persisted in SQLite via LangGraph checkpointing

**Key Concepts:**
- `StateGraph`, `TypedDict` state
- Nodes as Python functions
- `START`, `END`, conditional edges
- `ToolNode` for structured outputs
- LangGraph `MemorySaver` vs `SqliteSaver` checkpointing
- Structured output with Pydantic models as tool schemas
- Visualizing the graph with Mermaid

**File Structure:**
```
part_05_first_agent/
├── agent/
│   ├── state.py        # TypedDict state definition
│   ├── nodes.py        # All node functions
│   ├── edges.py        # Conditional edge logic
│   ├── graph.py        # Graph assembly
│   └── tools.py        # Tools available to agent
├── checkpointing/
│   └── sqlite_saver.py # SQLite persistence for state
├── main.py             # FastAPI endpoint to invoke agent
├── run_demo.py         # CLI demo runner
├── tests/
│   └── test_triage_agent.py
└── README.md
```

**Acceptance Criteria:**
- [ ] Agent correctly routes high-urgency cases
- [ ] State is persisted across multi-turn conversations
- [ ] Graph visualization renders as Mermaid diagram
- [ ] Agent handles edge cases (ambiguous symptoms, missing info)

---

### PART 6 — Multi-Agent Orchestration
**📁 `part_06_multi_agent/`**

**Goal:** Build a supervisor agent that routes to specialized sub-agents: Appointment Agent, Billing Agent, Medical Records Agent, and Triage Agent.

**What You Build:**
- Supervisor agent with intent classification
- 4 specialized sub-agents as separate LangGraph graphs
- Supervisor → sub-agent routing with `Send` API
- Shared state handoff between agents
- Fallback agent for unhandled intents

**Architecture:**
```
User Query
    ↓
Supervisor Agent (intent classification)
    ├── appointment_intent  → Appointment Agent
    ├── billing_intent      → Billing Agent  
    ├── records_intent      → Medical Records Agent
    ├── triage_intent       → Triage Agent
    └── unknown_intent      → General Agent
```

**Key Concepts:**
- Multi-agent with supervisor pattern
- LangGraph `Send` API for parallel sub-agent invocation
- Agent-as-tool pattern
- Shared vs. isolated state
- Error propagation across agents
- Agent handoff protocols

**File Structure:**
```
part_06_multi_agent/
├── agents/
│   ├── supervisor.py
│   ├── appointment_agent.py
│   ├── billing_agent.py
│   ├── records_agent.py
│   └── triage_agent.py
├── orchestrator/
│   ├── graph.py        # Top-level graph with supervisor
│   ├── router.py       # Intent classification & routing
│   └── state.py        # Shared state schema
├── main.py
├── tests/
│   └── test_multi_agent.py
└── README.md
```

**Acceptance Criteria:**
- [ ] Supervisor correctly classifies 10+ test intents
- [ ] Each sub-agent handles its domain independently
- [ ] State flows correctly from supervisor to sub-agent and back
- [ ] Unrecognized intents are handled gracefully

---

### PART 7 — Tool Calling & Function Execution
**📁 `part_07_tool_calling/`**

**Goal:** Equip agents with real tools — database queries, API calls, calculations, and external service integrations.

**What You Build:**
- Custom LangChain tools: `get_patient_by_id`, `schedule_appointment`, `calculate_bill`, `search_drug_interactions`
- Tool schemas defined with Pydantic
- Agent with tool-use loop (ReAct pattern)
- Parallel tool execution
- Tool error handling and retry logic

**Key Concepts:**
- `@tool` decorator and `StructuredTool`
- Pydantic tool input schemas
- `ToolNode` in LangGraph
- ReAct (Reasoning + Acting) agent pattern
- Parallel tool calls with `asyncio.gather`
- Tool execution timeout and error wrapping
- Injecting dependencies into tools (DB session)

**File Structure:**
```
part_07_tool_calling/
├── tools/
│   ├── patient_tools.py     # DB-backed patient tools
│   ├── appointment_tools.py
│   ├── billing_tools.py
│   ├── medical_tools.py     # Drug lookup, ICD codes
│   └── utility_tools.py     # Date calc, formatting
├── agent/
│   ├── react_agent.py       # ReAct loop implementation
│   └── graph.py
├── main.py
├── tests/
│   └── test_tools.py
└── README.md
```

**Acceptance Criteria:**
- [ ] All tools have typed Pydantic input schemas
- [ ] Agent correctly invokes multiple tools in a single run
- [ ] Tool failures are caught and reported to the agent
- [ ] Parallel tool execution works for independent calls

---

### PART 8 — Memory, Session State & Conversation History
**📁 `part_08_memory_state/`**

**Goal:** Give agents short-term (in-session) and long-term (cross-session) memory. Implement patient context retention.

**What You Build:**
- In-memory conversation buffer (short-term)
- SQLite-backed long-term memory (summarized patient history)
- Semantic memory: store patient preferences, past complaints as embeddings in Qdrant
- Memory retrieval: inject relevant past context into agent prompts
- Session management API (create, resume, list sessions)

**Key Concepts:**
- LangGraph `SqliteSaver` for thread-level checkpointing
- `thread_id` for session isolation
- Conversation summarization with LLM
- Episodic vs. semantic memory
- `VectorStoreMemory` with Qdrant
- Memory window management (trimming old context)
- Cross-session profile building

**File Structure:**
```
part_08_memory_state/
├── memory/
│   ├── short_term.py       # In-context window management
│   ├── long_term.py        # SQLite summarized history
│   ├── semantic.py         # Qdrant-backed semantic memory
│   └── manager.py          # Unified memory interface
├── sessions/
│   ├── session_store.py    # SQLite session persistence
│   └── session_api.py      # CRUD for sessions
├── agent/
│   ├── memory_agent.py     # Agent with all memory types
│   └── graph.py
├── main.py
├── tests/
│   └── test_memory.py
└── README.md
```

**Acceptance Criteria:**
- [ ] Agent remembers patient name across turns in a session
- [ ] Long-term memory summarizes after 10+ messages
- [ ] Resuming a `thread_id` restores previous context
- [ ] Semantic search retrieves relevant past interactions

---

### PART 9 — Human-in-the-Loop Workflows
**📁 `part_09_human_in_loop/`**

**Goal:** Build approval workflows where agents pause, await human review, and resume. Critical for medical decision-making.

**What You Build:**
- Agent that pauses before high-risk actions (prescribing medication, large billing adjustments)
- Async approval endpoint: `POST /approve/{run_id}`
- Rejection with feedback: agent re-routes based on rejection reason
- Timeout handling (auto-escalate if no approval in 5 min)
- Audit trail of all human interventions

**Key Concepts:**
- LangGraph `interrupt()` for pause/resume
- LangGraph `Command` with `update` for resuming with input
- Persistent run state during interruption (SQLite)
- Webhook / polling pattern for approval notification
- Optimistic vs. pessimistic interrupt strategies

**File Structure:**
```
part_09_human_in_loop/
├── workflows/
│   ├── prescription_workflow.py  # Requires doctor approval
│   ├── billing_workflow.py       # Requires admin approval
│   └── discharge_workflow.py     # Requires sign-off
├── approval/
│   ├── approval_store.py    # Pending approvals in SQLite
│   ├── approval_api.py      # FastAPI approval endpoints
│   └── notifier.py          # Notification stubs
├── agent/
│   ├── hitl_agent.py
│   └── graph.py
├── main.py
├── tests/
│   └── test_hitl.py
└── README.md
```

**Acceptance Criteria:**
- [ ] Agent pauses at interrupt points and persists state
- [ ] `POST /approve/{run_id}` resumes execution correctly
- [ ] Rejected runs re-route with rejection context injected
- [ ] Audit log records every interrupt, approve, and reject event

---

### PART 10 — Streaming Responses & Server-Sent Events
**📁 `part_10_streaming/`**

**Goal:** Stream LLM tokens and agent progress events to the frontend in real-time using SSE.

**What You Build:**
- Streaming chat endpoint with `StreamingResponse`
- Agent event streaming (node transitions, tool calls, LLM tokens)
- SSE event types: `token`, `tool_start`, `tool_end`, `agent_step`, `done`, `error`
- Simple HTML/JS frontend consuming the SSE stream
- Backpressure handling for slow clients

**Key Concepts:**
- LangChain `astream_events()` API (v2)
- FastAPI `StreamingResponse` with `EventSourceResponse`
- `sse-starlette` library
- Event filtering and formatting
- LangGraph streaming mode (`values`, `updates`, `debug`)
- Async generator patterns

**File Structure:**
```
part_10_streaming/
├── streaming/
│   ├── event_types.py      # SSE event schema definitions
│   ├── event_formatter.py  # Format LangGraph events → SSE
│   └── stream_handler.py   # Async generator for SSE
├── agent/
│   └── streaming_agent.py
├── frontend/
│   └── index.html          # Simple SSE demo UI
├── main.py
├── tests/
│   └── test_streaming.py
└── README.md
```

**Acceptance Criteria:**
- [ ] Tokens stream in real-time (not buffered)
- [ ] All agent event types are correctly mapped and emitted
- [ ] Frontend demo shows live streaming
- [ ] Stream closes cleanly on `done` or `error` events

---

### PART 11 — Testing AI Agents & RAG Pipelines
**📁 `part_11_testing/`**

**Goal:** Write a proper test suite for AI systems — unit, integration, and evaluation tests.

**What You Build:**
- Unit tests for tools, nodes, and validators
- Integration tests for full agent runs (deterministic mock LLM)
- RAG evaluation: relevance, faithfulness, and answer correctness metrics
- Pytest fixtures for agent/DB/Qdrant setup and teardown
- CI-friendly test configuration (no real API calls in unit tests)

**Key Concepts:**
- Mocking LLM calls with `langchain_core.fake_llm`
- `pytest-asyncio` for async tests
- `pytest.fixture` with `anyio_backend`
- LangChain `FakeListChatModel` for deterministic responses
- RAG evaluation with `RAGAS` library
- Test database isolation (in-memory SQLite per test)
- Evaluating agent traces with LangSmith datasets

**File Structure:**
```
part_11_testing/
├── tests/
│   ├── conftest.py             # Shared fixtures
│   ├── unit/
│   │   ├── test_tools.py
│   │   ├── test_nodes.py
│   │   └── test_validators.py
│   ├── integration/
│   │   ├── test_agent_flows.py
│   │   └── test_rag_pipeline.py
│   └── evaluation/
│       ├── test_rag_quality.py # RAGAS metrics
│       └── test_agent_correctness.py
├── fixtures/
│   ├── sample_queries.json
│   └── expected_outputs.json
├── pytest.ini
└── README.md
```

**Acceptance Criteria:**
- [ ] Unit tests run without any API key
- [ ] Integration tests mock LLM with deterministic responses
- [ ] RAG evaluation scores: relevance > 0.7, faithfulness > 0.8
- [ ] Test suite runs in < 60 seconds (unit + integration)

---

### PART 12 — Observability with LangSmith
**📁 `part_12_observability/`**

**Goal:** Instrument all agents and chains with LangSmith tracing. Build a custom monitoring dashboard.

**What You Build:**
- LangSmith tracing on all agents and RAG chains
- Custom run metadata tagging (patient_id, session_id, agent_type)
- LangSmith dataset creation for regression testing
- Token usage and latency dashboards
- Alerting on failure rates (stub with logging)

**Key Concepts:**
- `LANGCHAIN_TRACING_V2` env setup
- `@traceable` decorator for custom functions
- Run metadata and tags
- LangSmith `Client` for programmatic dataset management
- Feedback API for human evaluation scores
- Cost tracking per agent run

**File Structure:**
```
part_12_observability/
├── tracing/
│   ├── setup.py            # LangSmith initialization
│   ├── decorators.py       # Custom @traceable wrappers
│   └── metadata.py         # Standard metadata builders
├── monitoring/
│   ├── metrics.py          # Token usage, latency tracking
│   └── alerts.py           # Failure detection stubs
├── evaluation/
│   ├── dataset_builder.py  # Build LangSmith datasets
│   └── evaluator.py        # Run evaluations against datasets
├── main.py
└── README.md
```

**Acceptance Criteria:**
- [ ] All agent runs appear in LangSmith UI with correct metadata
- [ ] Token usage is tracked per run
- [ ] At least one LangSmith dataset with 20+ examples
- [ ] Evaluation runs show pass/fail per example

---

### PART 13 — Production Deployment Patterns
**📁 `part_13_production_deploy/`**

**Goal:** Package and deploy the hospital AI system production-ready. Covers Docker, config management, security, and scalability.

**What You Build:**
- Multi-service Docker Compose (FastAPI app + Qdrant + SQLite viewer)
- Production `Dockerfile` with multi-stage build
- Environment-based config management (dev / staging / prod profiles)
- API key rotation and secrets management pattern
- Rate limiting with `slowapi`
- Background task queue for async agent runs (FastAPI `BackgroundTasks`)
- Health checks, liveness and readiness probes
- Graceful shutdown handling

**Key Concepts:**
- Docker multi-stage builds for small images
- `Pydantic BaseSettings` with env-prefix overrides
- FastAPI `BackgroundTasks` vs Celery
- `slowapi` for rate limiting
- CORS, trusted hosts middleware
- SQLite WAL mode for concurrent access
- Qdrant persistent volumes

**File Structure:**
```
part_13_production_deploy/
├── Dockerfile
├── docker-compose.yml
├── docker-compose.prod.yml
├── config/
│   ├── settings.py         # Full production settings
│   ├── dev.env
│   └── prod.env.example
├── middleware/
│   ├── rate_limit.py
│   ├── logging.py
│   └── error_handler.py
├── tasks/
│   └── background_tasks.py
├── health/
│   └── health_router.py    # Liveness / readiness checks
├── scripts/
│   ├── start.sh
│   └── migrate.sh
└── README.md
```

**Acceptance Criteria:**
- [ ] `docker-compose up` starts all services successfully
- [ ] App handles 50 concurrent requests without errors
- [ ] Rate limiting rejects requests above threshold
- [ ] Health check endpoints return correct statuses
- [ ] Secrets never logged or exposed in error messages

---

### PART 14 — Capstone: Full Hospital Intelligence Platform
**📁 `part_14_capstone/`**

**Goal:** Integrate all 13 parts into a single, fully operational Hospital AI Platform.

**What You Build:**
- Unified FastAPI application with all agents integrated
- Complete patient journey: walk-in → triage → appointment → consultation → prescription → billing → discharge
- Full RAG over hospital knowledge base
- Multi-agent orchestration with human-in-the-loop for critical decisions
- Streaming chat interface
- SQLite for all persistence + Qdrant for semantic search
- LangSmith tracing on every agent run
- Production Docker deployment

**Patient Journey Flow:**
```
1. Patient arrives (intake form → Pydantic validation)
2. Triage Agent assesses urgency
3. Appointment Agent schedules with available doctor
4. Medical Records Agent pulls patient history via RAG
5. Consultation Agent assists doctor with diagnosis suggestions
6. Prescription Agent drafts prescription → Human-in-Loop (doctor approval)
7. Billing Agent calculates charges → Human-in-Loop (patient confirmation)
8. Discharge Agent creates summary and follow-up instructions
```

**API Surface:**
```
POST   /patients                    # Register new patient
POST   /sessions/{patient_id}       # Start AI session
POST   /sessions/{session_id}/chat  # Chat with streaming
GET    /sessions/{session_id}/state # Get current session state
POST   /approvals/{run_id}          # Approve/reject HITL action
GET    /patients/{id}/history       # Get patient history
GET    /search                      # Semantic search over docs
GET    /health                      # Full health check
```

---

## 6. Shared Infrastructure Specification

### Shared Models (`shared/models/`)

```python
# All parts import from here
from shared.models.patient import Patient, PatientCreate
from shared.models.doctor import Doctor
from shared.models.appointment import Appointment, AppointmentStatus
from shared.models.medical_record import MedicalRecord
from shared.models.billing import Invoice, BillingItem
```

### Shared Config (`shared/config.py`)

```python
class Settings(BaseSettings):
    # LLM
    openai_api_key: str
    anthropic_api_key: str = ""
    llm_model: str = "gpt-4o"
    embedding_model: str = "text-embedding-3-small"
    
    # Qdrant
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "hospital_docs"
    
    # Database
    database_url: str = "sqlite+aiosqlite:///./hospital.db"
    
    # LangSmith
    langchain_tracing_v2: bool = False
    langchain_api_key: str = ""
    langchain_project: str = "hospital-ai"
    
    # App
    environment: str = "development"
    log_level: str = "INFO"
    
    model_config = ConfigDict(env_file=".env")
```

### Docker Compose (root level)

```yaml
services:
  qdrant:
    image: qdrant/qdrant:latest
    ports: ["6333:6333"]
    volumes: ["qdrant_storage:/qdrant/storage"]
  
  sqlite-web:
    image: coleifer/sqlite-web
    ports: ["8080:8080"]
    volumes: ["./hospital.db:/data/hospital.db"]
```

---

## 7. Non-Functional Requirements

| Category | Requirement |
|----------|------------|
| **Performance** | Agent responses < 5s for standard queries |
| **Reliability** | Graceful fallback when LLM API is unavailable |
| **Security** | No PII logged; API keys via env vars only |
| **Maintainability** | Each part is self-contained and runnable independently |
| **Documentation** | Every part has a `README.md` with step-by-step instructions |
| **Testability** | Unit tests runnable without API keys using mocks |
| **Portability** | Runs on macOS, Linux, and Windows (WSL2) |
| **Reproducibility** | Pinned dependency versions; seed data for consistent state |

---

## 8. Learning Path & Estimated Time

| Part | Topic | Estimated Time | Difficulty |
|------|-------|---------------|------------|
| 1 | Foundations | 3h | 🟢 Beginner |
| 2 | Pydantic v2 | 2h | 🟢 Beginner |
| 3 | SQLite + SQLAlchemy | 3h | 🟡 Intermediate |
| 4 | RAG + Qdrant | 4h | 🟡 Intermediate |
| 5 | First Agent | 4h | 🟡 Intermediate |
| 6 | Multi-Agent | 5h | 🔴 Advanced |
| 7 | Tool Calling | 3h | 🟡 Intermediate |
| 8 | Memory & State | 4h | 🔴 Advanced |
| 9 | Human-in-Loop | 4h | 🔴 Advanced |
| 10 | Streaming | 3h | 🟡 Intermediate |
| 11 | Testing | 4h | 🟡 Intermediate |
| 12 | Observability | 2h | 🟡 Intermediate |
| 13 | Production Deploy | 3h | 🟡 Intermediate |
| 14 | Capstone | 8h | 🔴 Advanced |
| **Total** | | **~52 hours** | |

---

## 9. Sample Data & Fixtures

Each part ships with:

- **5 sample patients** with realistic demographics
- **3 doctors** (cardiologist, GP, neurologist)
- **10 pre-ingested hospital documents** for RAG (policy PDFs, drug reference sheets, clinical guidelines)
- **Test conversation scripts** for agent demos
- **Postman/Bruno collection** for all API endpoints

---

## 10. Prerequisites for Learners

| Skill | Required Level |
|-------|---------------|
| Python | Intermediate (async/await, decorators, type hints) |
| REST APIs | Basic (understand HTTP methods, status codes) |
| SQL | Basic (SELECT, INSERT, JOIN) |
| Git | Basic (clone, commit, branch) |
| Docker | Basic (run containers, docker-compose up) |
| LLMs | No prior experience needed |

---

## 11. Repository Setup Guide

```bash
# 1. Clone the repo
git clone https://github.com/your-org/hospital-ai-platform.git
cd hospital-ai-platform

# 2. Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 3. Install all dependencies
uv sync

# 4. Copy environment variables
cp .env.example .env
# Edit .env and add your OpenAI API key

# 5. Start infrastructure
docker-compose up -d

# 6. Start from Part 1
cd part_01_foundations
uvicorn main:app --reload

# 7. Open API docs
open http://localhost:8000/docs
```

---

## 12. Content Delivery Plan

| Milestone | Parts Included | Target Completion |
|-----------|---------------|-------------------|
| Phase 1: Core Foundations | Parts 1–3 | Week 1 |
| Phase 2: RAG & First Agent | Parts 4–5 | Week 2 |
| Phase 3: Multi-Agent Systems | Parts 6–8 | Week 3–4 |
| Phase 4: Production Patterns | Parts 9–13 | Week 5–6 |
| Phase 5: Capstone | Part 14 | Week 7 |

---

## 13. Success Metrics

| Metric | Target |
|--------|--------|
| Parts completable independently | 100% |
| Test coverage across all parts | > 70% |
| Capstone patient journey success rate | > 95% |
| Docker-compose cold start time | < 60 seconds |
| API response P95 latency | < 3 seconds |

---

## 14. Appendix: Key Design Decisions

### Why SQLite (not PostgreSQL)?
SQLite requires zero infrastructure setup for learning. Production deployment section covers migration path to PostgreSQL with SQLAlchemy (same ORM code).

### Why OpenAI + optional Anthropic?
OpenAI GPT-4o is the default for broad tooling compatibility. All LLM calls are abstracted behind a factory so learners can swap to Claude 3.5, Gemini, or local Ollama models by changing one env var.

### Why LangGraph (not raw LangChain agents)?
LangGraph offers explicit state machines, deterministic routing, and proper persistence — essential for production-grade agents. Raw `AgentExecutor` is shown in early parts for context, then migrated to LangGraph.

### Why Qdrant (not FAISS/Chroma)?
Qdrant is production-ready, supports filtering, hybrid search, and has a Docker image for local dev. The same LangChain `VectorStore` interface makes it trivial to swap providers.

### Why Hospital Domain?
Medical workflows have natural complexity: multi-step processes, human oversight requirements, diverse document types, strict validation, and high-stakes decisions. This forces learners to solve real production problems, not toy examples.

---

*This PRD is a living document. Each part's README may expand on its specification with additional learning notes, gotchas, and extension exercises.*