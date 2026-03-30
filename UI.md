# 📋 Product Requirements Document
## Hospital AI Platform — Tutorial Showcase Application
### Single React SPA · GitHub Pages · All 14 Parts in One App

---

> **Version:** 1.0.0
> **Status:** Draft
> **Type:** Single Page Application (SPA)
> **Hosting:** GitHub Pages — `https://<org>.github.io/hospital-ai-platform`
> **Stack:** React 18 · TypeScript · Vite · Tailwind CSS · React Router v6

---

## 1. Vision & Purpose

A **single, unified React application** that serves as the complete interactive showcase for the Hospital AI Platform tutorial series. Every concept, every API endpoint, every agent — all 14 parts — are accessible from one app without switching tabs or projects.

Learners run the FastAPI backend locally (`localhost:8000`) and use this UI as their **command center**: read theory, run live demos, track progress, and visualize agent behaviour — all from one screen.

---

## 2. Application Layout (Single Shell)

The entire app lives inside one persistent shell. Navigation never causes a full page reload.

```
┌─────────────────────────────────────────────────────────────────┐
│  TOPBAR                                                         │
│  🏥 Hospital AI Platform    [Parts ▾]  [Playground]  [Progress] │
│  ● Backend: Connected · localhost:8000          [☀/🌙] [GitHub] │
├───────────────┬─────────────────────────────────────────────────┤
│               │                                                 │
│  LEFT SIDEBAR │   MAIN CONTENT AREA                             │
│  (persistent) │   (changes based on active view)                │
│               │                                                 │
│  ─ Overview   │                                                 │
│  ─ Setup      │                                                 │
│               │                                                 │
│  PHASE 1      │                                                 │
│  01 Foundations                                                 │
│  02 Pydantic  │                                                 │
│  03 SQLite    │                                                 │
│               │                                                 │
│  PHASE 2      │                                                 │
│  04 RAG       │                                                 │
│  05 Agent     │                                                 │
│               │                                                 │
│  PHASE 3      │                                                 │
│  06 Multi-Agent                                                 │
│  07 Tools     │                                                 │
│  08 Memory    │                                                 │
│               │                                                 │
│  PHASE 4      │                                                 │
│  09 HITL      │                                                 │
│  10 Streaming │                                                 │
│  11 Testing   │                                                 │
│  12 Observ.   │                                                 │
│  13 Deploy    │                                                 │
│               │                                                 │
│  🏆 Capstone  │                                                 │
│  14 Full App  │                                                 │
│               │                                                 │
│  ─ Glossary   │                                                 │
│  ─ Progress   │                                                 │
└───────────────┴─────────────────────────────────────────────────┘
```

---

## 3. Routing Structure

All routes render inside the persistent shell (sidebar + topbar stay fixed).

```
/                          → Overview / Home dashboard
/setup                     → Environment setup checklist
/part/01                   → Part detail + embedded playground
/part/02
/part/03
  ...
/part/14
/playground                → Global full-screen playground (any endpoint)
/progress                  → Learner progress dashboard
/glossary                  → AI/ML terms reference
```

---

## 4. Tech Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Framework | React | 18+ |
| Language | TypeScript | 5+ |
| Build | Vite | 5+ |
| Styling | Tailwind CSS | 3+ |
| Routing | React Router v6 | 6+ |
| State | Zustand (localStorage persist) | 4+ |
| HTTP | Axios | Latest |
| Code Highlight | Shiki | Latest |
| Diagrams | Mermaid.js | Latest |
| Charts | Recharts | Latest |
| Animations | Framer Motion | 11+ |
| Icons | Lucide React | Latest |
| Markdown | react-markdown + remark-gfm | Latest |
| Deploy | gh-pages + GitHub Actions | Latest |

---

## 5. Views Specification

---

### VIEW 1 — Overview Dashboard (`/`)

The landing view inside the shell. Shows the entire platform at a glance.

**Layout: 3-row grid**

```
┌────────────────────────────────────────────────────┐
│  ROW 1 — Hero Banner                               │
│  "Hospital AI Platform"  · 14 Parts · ~52 Hours    │
│  Overall progress ring  [Continue →PartX]          │
├──────────────┬─────────────────┬───────────────────┤
│  ROW 2A      │  ROW 2B         │  ROW 2C           │
│  Phase Cards │  Tech Stack     │  Backend Status   │
│  (5 phases)  │  Grid           │  Health Panel     │
├────────────────────────────────────────────────────┤
│  ROW 3 — Part Cards Strip (horizontal scroll)      │
│  [01][02][03][04][05][06][07][08][09]....[14]      │
└────────────────────────────────────────────────────┘
```

**Components:**

**Hero Banner**
- Title + subtitle
- Circular progress ring: `X / 14 parts complete`
- Phase progress bar strip (5 coloured segments)
- `[Continue Learning →]` CTA — navigates to the next incomplete part

**Phase Summary Cards (5 cards)**
- Each card: phase name, colour, parts range, parts completed `X/Y`
- Click → scrolls sidebar to that phase

**Tech Stack Grid**
- Logo + name for each technology: Python, FastAPI, LangChain, LangGraph, Pydantic, SQLite, Qdrant, OpenAI API, LangSmith, Docker
- Hover shows short description

**Backend Status Panel**
- Live ping to `GET localhost:8000/health` every 5 seconds
- Shows: 🟢 Connected / 🔴 Disconnected
- If disconnected: shows setup command to start the server
- Response time display (ms)

**Part Cards Strip**
- Horizontal scrollable row of 14 cards
- Each card: number badge, title, difficulty chip, estimated time, status icon (locked/in-progress/done)
- Click → navigates to `/part/:id`

---

### VIEW 2 — Setup Guide (`/setup`)

Interactive pre-flight checklist before starting Part 1.

**Layout: 2 columns**

```
┌────────────────────────┬───────────────────────────┐
│  LEFT — Checklist      │  RIGHT — Commands          │
│                        │                            │
│  Prerequisites         │  Tab: macOS / Linux / Win  │
│  □ Python 3.11+        │                            │
│  □ uv installed        │  git clone ...             │
│  □ Docker running      │  cp .env.example .env      │
│  □ OpenAI API key      │  # Add OPENAI_API_KEY      │
│  □ Git installed       │  docker-compose up -d      │
│  □ VS Code / PyCharm   │  uv sync                   │
│                        │  uvicorn main:app --reload  │
│  0 / 6 complete        │                            │
│  [Start Part 1 →]      │  [Copy All Commands]       │
└────────────────────────┴───────────────────────────┘
```

**Sections:**

**Prerequisites Checklist**
- 6 checkable items stored in Zustand + localStorage
- Progress bar fills as items are checked
- `[Start Part 1 →]` button activates when all 6 are checked

**Tabbed Command Block**
- OS tabs: macOS · Linux · Windows (WSL2)
- Full setup commands with copy button per block
- Inline comments explaining each step

**Environment Variables Table**
- Variable · Required · Description · Where to get
- `OPENAI_API_KEY` — ✅ Required — GPT-4o + embeddings — platform.openai.com
- `LANGCHAIN_API_KEY` — ⚠️ Optional — LangSmith tracing — smith.langchain.com
- `QDRANT_URL` — ⚠️ Optional — Remote Qdrant — qdrant.io

**Verify Setup Terminal Block**
- Shows expected output of `python shared/verify_setup.py`
- Static code block — learner runs this in their terminal

**OpenAI Cost Estimator Widget**
- Input: requests per day slider
- Select: `gpt-4o` vs `gpt-4o-mini`
- Output: estimated monthly cost (calculated client-side using published token rates)

---

### VIEW 3 — Part Detail Page (`/part/:partId`)

The **core learning view**. Every part has identical layout — content changes.

**Layout: 2 columns + sticky right panel**

```
┌────────────────────────────────────┬──────────────────────┐
│  MAIN (scrollable)                 │  RIGHT PANEL (sticky) │
│                                    │                       │
│  A) Part Header                    │  Key Concepts List    │
│  B) What You'll Build              │  (anchored links)     │
│  C) Architecture Diagram           │  ───────────────────  │
│  D) Core Concepts (accordion)      │  Files In This Part   │
│  E) Step-by-Step Guide             │  (folder tree)        │
│  F) ── EMBEDDED PLAYGROUND ──      │  ───────────────────  │
│  G) Acceptance Criteria            │  Official Docs Links  │
│  H) Common Errors & Fixes          │  ───────────────────  │
│  I) Next Part CTA                  │  Completion           │
│                                    │  [✓ Mark Complete]    │
└────────────────────────────────────┴──────────────────────┘
```

**Section A — Part Header**
- Large part number + phase badge + difficulty chip
- Title, one-line goal
- Metadata row: ⏱ `3h` · 📁 `part_01_foundations/` · 🔗 GitHub folder link
- Breadcrumb: `Phase 1 > Part 1`
- Progress: previous part ← · → next part navigation arrows

**Section B — What You'll Build**
- Bullet list of endpoints/features
- Each endpoint shown as a method+path badge: `POST /ask` `GET /health`
- Visual preview card (static screenshot placeholder or diagram)

**Section C — Architecture Diagram**
- Mermaid diagram rendered inline, specific to each part
- Part 01: simple request flow · Part 05: LangGraph state machine · Part 06: multi-agent supervisor · etc.
- Zoom on click (modal)
- "Copy Mermaid source" button

**Section D — Core Concepts (Accordion)**
- Each concept is a collapsible card
- Inside: plain-English explanation + Shiki-highlighted code snippet
- Code snippet has: filename label + copy button + language badge
- Concepts link to glossary terms

**Section E — Step-by-Step Guide**
- Numbered steps: title + description + code block
- Each step has a micro-checkbox `□ Done`
- Progress indicator: `Step 3 of 7`
- Steps reference exact filenames in the monorepo

**Section F — Embedded Playground**
- Full inline playground (NOT a separate page — embedded in the part page)
- Collapsible header: `🔌 Live Playground — Try It Now`
- Backend status badge inline
- Shows only the endpoints relevant to this part
- Same UI as the Global Playground but scoped to part endpoints
- Detailed spec in Section 5 (Playground Component)

**Section G — Acceptance Criteria**
- Checkable list matching the backend PRD criteria
- Stored in Zustand per part
- Shows `X / Y criteria met`
- "Mark Part Complete" available only when all criteria checked

**Section H — Common Errors & Fixes**
- Collapsible table
- 3 columns: `Error` · `Cause` · `Fix`
- 3–5 rows per part with real errors learners hit

**Section I — Next Part CTA**
- Card at bottom: next part title, difficulty, time estimate
- `[Continue to Part X →]` button

---

### VIEW 4 — Playground Component (Embedded + Full-Screen)

Used in two contexts:
- **Embedded** inside each Part Detail page (scoped to that part's endpoints)
- **Full-Screen** at `/playground` (all endpoints from all parts)

**Layout:**

```
┌─────────────────────────────────────────────────────────┐
│  🟢 localhost:8000 · Connected · 142ms                  │
├────────────────┬────────────────────────────────────────┤
│  ENDPOINT LIST │  REQUEST / RESPONSE PANE               │
│                │                                        │
│  ▸ Part 1      │  Method: [POST ▾]  Path: /ask          │
│    GET /health │  ───────────────────────────────────── │
│  ● POST /ask   │  HEADERS         BODY          PARAMS  │
│    POST /summ  │  ─────────────── ────────────────────  │
│    POST /class │  {                                     │
│                │    "question": "What are ICU           │
│  ▸ Part 3      │     visiting hours?",                  │
│    GET /patient│    "patient_id": "P001"                │
│    POST /patie │  }                                     │
│    ...         │  ───────────────────────────────────── │
│                │  [▶ Send]  [Reset]  [Copy as cURL]     │
│                ├────────────────────────────────────────┤
│                │  RESPONSE                              │
│                │  ── 200 OK · 1.24s ─────────────────── │
│                │  {                                     │
│                │    "answer": "ICU visiting hours are   │
│                │     10am–8pm daily...",                │
│                │    "model": "gpt-4o",                  │
│                │    "tokens_used": 142                  │
│                │  }                                     │
│                ├────────────────────────────────────────┤
│                │  HISTORY  [Clear All]                  │
│                │  ✅ POST /ask → 200  1.2s  2min ago    │
│                │  ✅ GET /health → 200  0.1s  5min ago  │
└────────────────┴────────────────────────────────────────┘
```

**Playground Features:**

**Endpoint List (left panel)**
- Grouped by part when in full-screen mode
- Active endpoint highlighted
- Method badge colour: GET=green · POST=blue · PUT=amber · DELETE=red
- Search/filter box

**Request Pane (right top)**
- Method dropdown + path input
- Three tabs: Headers · Body · Params
- JSON editor with syntax highlighting + validation
- Inline JSON error messages
- Pre-filled example body per endpoint (from part data files)

**Action Bar**
- `[▶ Send]` — fires the API call via Axios
- `[Reset]` — restores example body
- `[Copy as cURL]` — copies full curl command to clipboard

**Response Pane (right bottom)**
- Status badge: `200 OK` (green) · `4xx` (amber) · `5xx` (red)
- Response time in ms
- JSON pretty-print with Shiki highlighting
- Copy response button

**Streaming Mode (Parts 10, 14)**
- Toggle: `⚡ Streaming Mode`
- Response pane switches to live token stream
- Tokens appear one by one as SSE events arrive
- Event type labels: `[token]` `[tool_start]` `[tool_end]` `[done]`
- Auto-scroll to bottom

**Request History**
- Last 10 requests stored in localStorage
- Shows: method, path, status, latency, timestamp
- Click to restore request body
- Clear all button

**Backend Disconnected State**
- Overlay shows: "⚠️ Backend not running"
- Shows `uvicorn main:app --reload` command to start
- Auto-reconnects when backend comes up (polling every 3s)

---

### VIEW 5 — Progress Dashboard (`/progress`)

Full picture of the learner's journey.

**Layout: Dashboard grid**

```
┌──────────────────┬────────────────┬─────────────────────┐
│  Overall         │  Time Spent    │  Next Up            │
│  Progress Ring   │  Estimate      │  Part X Card        │
│  X / 14 parts    │  ~Xh remaining │  [Continue →]       │
├──────────────────┴────────────────┴─────────────────────┤
│  PART GRID — 14 cards, 4 columns                        │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐                   │
│  │  01  │ │  02  │ │  03  │ │  04  │                   │
│  │  ✅  │ │  ✅  │ │  🔄  │ │  🔒  │                   │
│  └──────┘ └──────┘ └──────┘ └──────┘                   │
├─────────────────────────────────────────────────────────┤
│  SKILLS RADAR CHART                                     │
│  FastAPI · LangChain · LangGraph · RAG                  │
│  Pydantic · SQLite · Testing · Deployment               │
├─────────────────────────────────────────────────────────┤
│  ACCEPTANCE CRITERIA TRACKER                            │
│  X / 47 total criteria completed                        │
│  Progress bar per phase                                 │
└─────────────────────────────────────────────────────────┘
```

**Components:**

**Summary Stat Cards (top row)**
- Overall progress ring: `X / 14`
- Phase completion mini-bars (5 phases)
- Estimated hours remaining
- Next recommended part with CTA

**Part Grid (14 cards)**
- Status icons: ✅ Complete · 🔄 In Progress · 🔒 Locked · ⬜ Not Started
- Completion date for completed parts
- Criteria count: `4/4 ✓`
- Click → navigates to `/part/:id`

**Skills Radar Chart**
- Recharts `RadarChart` — 8 axes
- Skills and which parts contribute to each:
  - FastAPI ← Parts 1, 3, 9, 13
  - LangChain ← Parts 1, 4, 7
  - LangGraph ← Parts 5, 6, 8, 9
  - RAG/Qdrant ← Parts 4, 8
  - Pydantic ← Parts 1, 2
  - SQLite ← Parts 3, 5, 8
  - Testing ← Part 11
  - Deployment ← Part 13
- Fills in as parts are completed

**Acceptance Criteria Tracker**
- Grouped by phase
- Shows `X / Y` criteria met per phase
- Individual criteria items with checkboxes

**Reset Button**
- `[🗑 Reset All Progress]` — confirmation dialog — clears localStorage

---

### VIEW 6 — Glossary (`/glossary`)

Quick-reference dictionary for all AI/ML terms used in the series.

**Layout:**

```
┌────────────────────────────────────────────────────────┐
│  🔍 Search terms...                                    │
│  A  B  C  D  E  F  G  H  I  J  K  L  M  N  O  P  Q  R │
├────────────────────────────────────────────────────────┤
│                                                        │
│  A                                                     │
│  ┌──────────────────────────────────────────────────┐  │
│  │ Agent                                            │  │
│  │ An LLM that uses tools to take actions and       │  │
│  │ complete multi-step tasks autonomously.          │  │
│  │ Used in: [Part 5] [Part 6] [Part 7] [Part 14]   │  │
│  └──────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────┐  │
│  │ Agentic Loop                                     │  │
│  │ The observe → think → act cycle an LLM agent     │  │
│  │ repeats until the task is complete.              │  │
│  │ Used in: [Part 5] [Part 7]                       │  │
│  └──────────────────────────────────────────────────┘  │
│  ...                                                   │
└────────────────────────────────────────────────────────┘
```

**Features:**
- Client-side search filters terms in real time
- A–Z jump links
- Each term card: name + definition + "Used in" part badges (click to navigate)
- ~60 terms total: Agent, RAG, Vector DB, Embedding, LangGraph, LCEL, Tool Calling, Checkpointing, Pydantic, SQLAlchemy, Supervisor Pattern, ReAct, SSE, HITL, Qdrant, etc.

---

## 6. Persistent UI Elements

### Topbar (always visible)

```
┌──────────────────────────────────────────────────────────┐
│  🏥 Hospital AI  [Parts 1-14 ▾]  [Playground]  [Progress]│
│                          ● Connected · 142ms   [☀] [⭐GH] │
└──────────────────────────────────────────────────────────┘
```

- App logo + name (navigates to `/`)
- Parts dropdown: quick-jump to any part
- Playground shortcut (full-screen playground)
- Progress shortcut
- Backend status dot (live)
- Dark/light mode toggle
- GitHub repo star button

### Left Sidebar (always visible, collapsible on mobile)

```
Overview  [●]         ← dot = overall progress %
Setup     [✓]

──── Phase 1: Foundations ────
  01  Foundations      ✅
  02  Pydantic         ✅
  03  SQLite           🔄

──── Phase 2: RAG & Agents ────
  04  RAG + Qdrant     🔒
  05  First Agent      🔒

──── Phase 3: Multi-Agent ────
  06  Multi-Agent      🔒
  07  Tool Calling     🔒
  08  Memory           🔒

──── Phase 4: Production ────
  09  Human-in-Loop    🔒
  10  Streaming        🔒
  11  Testing          🔒
  12  Observability    🔒
  13  Deploy           🔒

──── Phase 5: Capstone ────
  14  Full Platform    🔒

Glossary
Progress
```

- Active part highlighted
- Completion icons: ✅ complete · 🔄 in progress · 🔒 locked
- Phase labels with phase colour
- Collapsible on mobile (hamburger trigger)

---

## 7. Component Architecture

```
src/
├── components/
│   │
│   ├── shell/
│   │   ├── AppShell.tsx          # Root layout: topbar + sidebar + main
│   │   ├── Topbar.tsx
│   │   ├── Sidebar.tsx
│   │   └── BackendStatusDot.tsx  # Live health ping indicator
│   │
│   ├── overview/
│   │   ├── HeroBanner.tsx
│   │   ├── PhaseCard.tsx
│   │   ├── TechStackGrid.tsx
│   │   ├── BackendStatusPanel.tsx
│   │   └── PartCardsStrip.tsx
│   │
│   ├── part/
│   │   ├── PartHeader.tsx
│   │   ├── WhatYouBuild.tsx
│   │   ├── ArchDiagram.tsx       # Mermaid renderer
│   │   ├── ConceptAccordion.tsx
│   │   ├── StepGuide.tsx
│   │   ├── AcceptanceCriteria.tsx
│   │   ├── ErrorsTable.tsx
│   │   └── NextPartCTA.tsx
│   │
│   ├── playground/
│   │   ├── Playground.tsx        # Main playground container
│   │   ├── EndpointList.tsx      # Left panel endpoint selector
│   │   ├── RequestPane.tsx       # Method + path + headers + body
│   │   ├── JsonEditor.tsx        # Shiki-powered JSON editor
│   │   ├── ResponsePane.tsx      # Response display
│   │   ├── StreamingPane.tsx     # SSE live token display
│   │   ├── RequestHistory.tsx    # Last 10 calls
│   │   └── CurlCopier.tsx
│   │
│   ├── progress/
│   │   ├── ProgressRing.tsx
│   │   ├── PartGrid.tsx
│   │   ├── SkillsRadar.tsx       # Recharts RadarChart
│   │   └── CriteriaTracker.tsx
│   │
│   ├── setup/
│   │   ├── PrereqChecklist.tsx
│   │   ├── CommandBlock.tsx      # OS-tabbed code block
│   │   ├── EnvVarsTable.tsx
│   │   └── CostEstimator.tsx
│   │
│   ├── glossary/
│   │   ├── GlossarySearch.tsx
│   │   ├── AlphaIndex.tsx
│   │   └── TermCard.tsx
│   │
│   └── ui/                       # Base design system
│       ├── Button.tsx
│       ├── Badge.tsx             # Difficulty · Phase · Status · Method
│       ├── CodeBlock.tsx         # Shiki highlighted + copy
│       ├── Tabs.tsx
│       ├── Accordion.tsx
│       ├── Modal.tsx
│       ├── Tooltip.tsx
│       ├── Toast.tsx
│       └── ProgressBar.tsx
│
├── pages/
│   ├── OverviewPage.tsx
│   ├── SetupPage.tsx
│   ├── PartDetailPage.tsx        # Renders any of 14 parts
│   ├── PlaygroundPage.tsx        # Full-screen playground
│   ├── ProgressPage.tsx
│   └── GlossaryPage.tsx
│
├── data/
│   ├── parts/
│   │   ├── part01.ts … part14.ts # Tutorial content per part
│   │   └── index.ts              # Re-exports all parts
│   ├── playgrounds/
│   │   ├── pg01.ts … pg14.ts     # Endpoint configs per part
│   │   └── index.ts
│   └── glossary.ts               # All 60+ glossary terms
│
├── store/
│   └── appStore.ts               # Zustand store (progress + prefs)
│
├── hooks/
│   ├── useBackendStatus.ts       # Polls /health every 5s
│   ├── useProgress.ts            # Reads/writes progress state
│   └── useTheme.ts               # Dark/light toggle
│
├── lib/
│   ├── api.ts                    # Axios instance → localhost:8000
│   └── mermaid.ts                # Mermaid init helper
│
├── App.tsx                       # Router setup
├── main.tsx
└── index.css
```

---

## 8. State Management

Single Zustand store, fully persisted to `localStorage`:

```typescript
interface AppStore {
  // Theme
  theme: "dark" | "light";
  setTheme: (t: "dark" | "light") => void;

  // Setup
  setupChecklist: Record<string, boolean>;   // prerequisite item id → checked
  toggleSetupItem: (id: string) => void;

  // Progress
  completedParts: string[];                  // ["01", "02"]
  completedCriteria: Record<string, string[]>; // partId → criteria ids
  markPartComplete: (partId: string) => void;
  toggleCriteria: (partId: string, criteriaId: string) => void;
  isPartUnlocked: (partId: string) => boolean;
  getOverallProgress: () => number;           // 0–100

  // Playground
  requestHistory: RequestHistoryItem[];
  addToHistory: (item: RequestHistoryItem) => void;
  clearHistory: () => void;

  // Reset
  resetAll: () => void;
}
```

---

## 9. Data Shape — Part Content File

```typescript
// src/data/parts/part05.ts — example
export const part05: PartData = {
  id: "05",
  title: "First LangGraph Agent",
  goal: "Build a stateful hospital triage agent with LangGraph.",
  phase: 2,
  phaseLabel: "RAG & First Agent",
  folder: "part_05_first_agent",
  estimatedHours: 4,
  difficulty: "intermediate",          // "beginner" | "intermediate" | "advanced"
  prerequisites: ["01", "02", "03", "04"],
  unlocks: ["06"],

  whatYouBuild: [
    { label: "POST /triage", description: "Start a triage session" },
    { label: "POST /triage/{id}/message", description: "Send symptom message" },
    { label: "GET /triage/{id}/state", description: "Get agent state" }
  ],

  mermaidDiagram: `
    stateDiagram-v2
      [*] --> intake
      intake --> symptom_analysis
      symptom_analysis --> urgency_check
      urgency_check --> high_urgency: score >= 7
      urgency_check --> low_urgency: score < 7
      high_urgency --> alert_doctor
      low_urgency --> schedule_appointment
      alert_doctor --> [*]
      schedule_appointment --> [*]
  `,

  concepts: [
    {
      id: "state-graph",
      title: "LangGraph StateGraph",
      explanation: "StateGraph defines the agent as a directed graph of nodes...",
      code: {
        language: "python",
        filename: "agent/graph.py",
        snippet: `from langgraph.graph import StateGraph, START, END
from agent.state import TriageState

graph = StateGraph(TriageState)
graph.add_node("intake", intake_node)
graph.add_node("symptom_analysis", analysis_node)
graph.add_edge(START, "intake")`
      }
    }
    // ...more concepts
  ],

  steps: [
    {
      number: 1,
      title: "Define agent state",
      description: "Create a TypedDict that holds all agent state fields...",
      code: { language: "python", filename: "agent/state.py",
        snippet: `from typing import TypedDict, Annotated
class TriageState(TypedDict):
    messages: Annotated[list, add_messages]
    patient_id: str
    urgency_score: int | None` }
    }
    // ...more steps
  ],

  acceptanceCriteria: [
    { id: "ac1", text: "Agent correctly routes high-urgency cases" },
    { id: "ac2", text: "State is persisted across multi-turn conversations" },
    { id: "ac3", text: "Graph visualization renders as Mermaid diagram" },
    { id: "ac4", text: "Agent handles edge cases (ambiguous symptoms)" }
  ],

  gotchas: [
    {
      error: "RecursionError: maximum graph depth exceeded",
      cause: "Missing END edge in graph definition",
      fix: "Add graph.add_edge('final_node', END) in graph.py"
    }
  ],

  resources: [
    { title: "LangGraph Docs", url: "https://langchain-ai.github.io/langgraph/" },
    { title: "StateGraph API", url: "https://langchain-ai.github.io/langgraph/reference/graphs/" }
  ]
};
```

---

## 10. Playground Endpoint Config Shape

```typescript
// src/data/playgrounds/pg05.ts
export const pg05: PlaygroundConfig = {
  partId: "05",
  endpoints: [
    {
      id: "start-triage",
      method: "POST",
      path: "/triage",
      description: "Start a new triage session for a patient",
      exampleBody: {
        patient_id: "P001",
        chief_complaint: "Chest pain radiating to left arm, started 2 hours ago"
      },
      streaming: false
    },
    {
      id: "send-message",
      method: "POST",
      path: "/triage/{session_id}/message",
      description: "Send a follow-up symptom message to the triage agent",
      pathParams: [{ name: "session_id", example: "sess_abc123" }],
      exampleBody: { message: "The pain is a 8/10 and I feel nauseous" },
      streaming: false
    },
    {
      id: "get-state",
      method: "GET",
      path: "/triage/{session_id}/state",
      description: "Get current triage session state and urgency score",
      pathParams: [{ name: "session_id", example: "sess_abc123" }],
      exampleBody: null,
      streaming: false
    }
  ]
};
```

---

## 11. GitHub Pages Deployment

### Vite Config

```typescript
// vite.config.ts
export default defineConfig({
  base: "/hospital-ai-platform/",
  plugins: [react()],
  build: {
    outDir: "dist",
    rollupOptions: {
      output: {
        manualChunks: {
          vendor:  ["react", "react-dom", "react-router-dom"],
          charts:  ["recharts"],
          code:    ["shiki"],
          motion:  ["framer-motion"],
          diagrams:["mermaid"]
        }
      }
    }
  }
});
```

### GitHub Actions (`.github/workflows/deploy-ui.yml`)

```yaml
name: Deploy UI to GitHub Pages

on:
  push:
    branches: [main]
    paths: ["ui/**"]

permissions:
  contents: write

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: "npm"
          cache-dependency-path: ui/package-lock.json
      - name: Install
        run: cd ui && npm ci
      - name: Build
        run: cd ui && npm run build
      - name: Deploy
        uses: peaceiris/actions-gh-pages@v4
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./ui/dist
```

### Package Scripts

```json
{
  "scripts": {
    "dev":     "vite",
    "build":   "tsc && vite build",
    "preview": "vite preview",
    "test":    "vitest run",
    "lint":    "eslint src --ext ts,tsx --fix"
  }
}
```

---

## 12. Design System

### Colours (Tailwind CSS custom tokens)

```js
// tailwind.config.ts
colors: {
  brand:   { DEFAULT: "#6366f1", dark: "#4f46e5" },   // Indigo — primary
  agent:   { DEFAULT: "#8b5cf6" },                     // Purple — LangGraph
  success: { DEFAULT: "#10b981" },                     // Emerald — complete
  warn:    { DEFAULT: "#f59e0b" },                     // Amber — in progress
  danger:  { DEFAULT: "#ef4444" },                     // Red — error / advanced
  surface: { 1: "#0f172a", 2: "#1e293b", 3: "#334155" }
}
```

### Phase Colour Map

| Phase | Label | Colour |
|-------|-------|--------|
| 1 | Core Foundations | `blue-500` |
| 2 | RAG & First Agent | `purple-500` |
| 3 | Multi-Agent Systems | `orange-500` |
| 4 | Production Patterns | `red-500` |
| 5 | Capstone | `yellow-500` |

### Difficulty Badge

| Level | Tailwind |
|-------|---------|
| Beginner | `bg-emerald-500/20 text-emerald-400` |
| Intermediate | `bg-amber-500/20 text-amber-400` |
| Advanced | `bg-red-500/20 text-red-400` |

### HTTP Method Badge

| Method | Tailwind |
|--------|---------|
| GET | `bg-green-500/20 text-green-400` |
| POST | `bg-blue-500/20 text-blue-400` |
| PUT | `bg-amber-500/20 text-amber-400` |
| DELETE | `bg-red-500/20 text-red-400` |

### Typography

```css
--font-sans: "Inter", system-ui, sans-serif;
--font-mono: "JetBrains Mono", "Fira Code", monospace;
```

---

## 13. Non-Functional Requirements

| Category | Requirement |
|----------|------------|
| Performance | Lighthouse score > 90 |
| Bundle | Initial JS < 200 KB gzipped |
| Accessibility | WCAG 2.1 AA |
| Offline | Part content readable offline (service worker) |
| Privacy | No analytics/tracking; all data in localStorage |
| CORS | FastAPI backend must have `localhost` in CORS origins |
| Responsive | Fully usable at 768px (tablet) and 375px (mobile) |
| Browser | Chrome 100+ · Firefox 100+ · Safari 15+ · Edge 100+ |

---

## 14. Build Milestones

| Milestone | Deliverable | Days |
|-----------|------------|------|
| M1 | AppShell + routing + sidebar + topbar | 1 |
| M2 | Overview dashboard (hero + part cards + backend status) | 1.5 |
| M3 | Part detail page layout + code blocks + Mermaid | 2 |
| M4 | Playground component (JSON editor + request/response) | 2.5 |
| M5 | Streaming playground (SSE token display) | 1 |
| M6 | Progress dashboard (radar chart + part grid) | 1.5 |
| M7 | Setup guide + glossary | 1 |
| M8 | All 14 part data files populated | 3 |
| M9 | Dark mode + animations + mobile responsive | 1.5 |
| M10 | GitHub Actions deploy pipeline | 0.5 |
| **Total** | | **~15.5 days** |

---

## 15. Success Metrics

| Metric | Target |
|--------|--------|
| Lighthouse Performance | ≥ 90 |
| Initial load time | < 1.5s |
| Client-side navigation | < 150ms |
| All 14 parts have content | 100% |
| Playground works for all endpoint types | 100% |
| Mobile usability (375px) | Fully functional |

---

*This is the single authoritative PRD for the Hospital AI Platform Tutorial Showcase UI. The backend monorepo spec lives in `PRD_Backend_Hospital_AI.md`.*