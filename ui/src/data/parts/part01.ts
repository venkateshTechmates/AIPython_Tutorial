import type { PartData } from "../../types";

export const part01: PartData = {
  id: "01",
  title: "FastAPI Foundations",
  goal: "Build your first production-ready FastAPI application with LangChain and OpenAI.",
  phase: 1,
  phaseLabel: "Core Foundations",
  folder: "part_01_foundations",
  estimatedHours: 3,
  difficulty: "beginner",
  prerequisites: [],
  unlocks: ["02"],
  whatYouBuild: [
    { label: "POST /ask", description: "Answer patient questions using GPT-4o" },
    { label: "POST /summarise", description: "Summarise clinical notes" },
    { label: "POST /classify", description: "Classify medical query intent" },
    { label: "GET /health", description: "Health check endpoint" },
  ],
  mermaidDiagram: `
flowchart LR
  Client -->|POST /ask| FastAPI
  FastAPI -->|LLMChain| LangChain
  LangChain -->|ChatOpenAI| OpenAI
  OpenAI -->|GPT-4o response| LangChain
  LangChain -->|answer + tokens| FastAPI
  FastAPI -->|JSON response| Client
  `,
  concepts: [
    {
      id: "fastapi-basics",
      title: "FastAPI Application Setup",
      explanation:
        "FastAPI is a modern Python web framework that uses Python type hints for automatic request/response validation. It generates OpenAPI docs automatically and is fully async.",
      code: {
        language: "python",
        filename: "main.py",
        snippet: `from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Hospital AI")

class AskRequest(BaseModel):
    question: str
    patient_id: str | None = None

@app.post("/ask")
async def ask(req: AskRequest):
    # LangChain processes the question
    answer = await chain.ainvoke({"question": req.question})
    return {"answer": answer, "model": "gpt-4o"}`,
      },
      glossaryTerms: ["FastAPI", "Pydantic", "OpenAPI"],
    },
    {
      id: "langchain-basics",
      title: "LangChain LCEL Chains",
      explanation:
        "LangChain Expression Language (LCEL) uses the pipe operator to compose prompts, models, and output parsers into a chain. The chain is fully async and streamable.",
      code: {
        language: "python",
        filename: "agent/chain.py",
        snippet: `from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-4o", temperature=0.3)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a hospital AI assistant."),
    ("human", "{question}")
])

chain = prompt | llm | StrOutputParser()

# Usage:
answer = await chain.ainvoke({"question": "What are ICU hours?"})`,
      },
      glossaryTerms: ["LCEL", "LangChain", "Chain"],
    },
    {
      id: "async-fastapi",
      title: "Async/Await in FastAPI",
      explanation:
        "FastAPI routes can be async, enabling concurrent request handling. Use async/await with LangChain's ainvoke() for non-blocking LLM calls.",
      code: {
        language: "python",
        filename: "main.py",
        snippet: `# Async route handles many concurrent requests
@app.post("/summarise")
async def summarise(req: SummariseRequest):
    # Non-blocking LLM call
    summary = await summarise_chain.ainvoke({
        "notes": req.clinical_notes
    })
    return {"summary": summary}`,
      },
    },
  ],
  steps: [
    {
      number: 1,
      title: "Set up the project",
      description:
        "Create the part_01_foundations/ directory and install dependencies with uv.",
      code: {
        language: "bash",
        filename: "terminal",
        snippet: `mkdir part_01_foundations && cd part_01_foundations
uv init --python 3.11
uv add fastapi uvicorn langchain langchain-openai pydantic`,
      },
    },
    {
      number: 2,
      title: "Define request/response schemas",
      description:
        "Use Pydantic BaseModel to define typed request and response shapes.",
      code: {
        language: "python",
        filename: "main.py",
        snippet: `from pydantic import BaseModel, Field

class AskRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=500)
    patient_id: str | None = None

class AskResponse(BaseModel):
    answer: str
    model: str
    tokens_used: int`,
      },
    },
    {
      number: 3,
      title: "Build the LangChain pipeline",
      description: "Create a reusable LCEL chain with system prompt and GPT-4o.",
      code: {
        language: "python",
        filename: "agent/chain.py",
        snippet: `SYSTEM_PROMPT = """You are an AI assistant for City General Hospital.
Answer questions about hospital services, policies, and general medical info.
Always recommend consulting a doctor for specific medical advice."""

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "{question}")
])

chain = prompt | ChatOpenAI(model="gpt-4o") | StrOutputParser()`,
      },
    },
    {
      number: 4,
      title: "Wire up FastAPI endpoints",
      description: "Create the POST /ask, POST /summarise, and POST /classify routes.",
    },
    {
      number: 5,
      title: "Run and test the server",
      description: "Launch with uvicorn and verify endpoints in the playground.",
      code: {
        language: "bash",
        filename: "terminal",
        snippet: `uvicorn main:app --reload --port 8000
# Open: http://localhost:8000/docs`,
      },
    },
  ],
  acceptanceCriteria: [
    { id: "ac1", text: "POST /ask returns an LLM-generated answer with token count" },
    { id: "ac2", text: "POST /summarise condenses clinical notes to ≤3 sentences" },
    { id: "ac3", text: "POST /classify returns an intent label from a fixed set" },
    { id: "ac4", text: "GET /health returns 200 with status: ok" },
    { id: "ac5", text: "All endpoints validated by Pydantic (422 on invalid input)" },
  ],
  gotchas: [
    {
      error: "openai.AuthenticationError: Invalid API key",
      cause: "OPENAI_API_KEY not set in environment",
      fix: "Add OPENAI_API_KEY to .env file and restart the server",
    },
    {
      error: "422 Unprocessable Entity on POST /ask",
      cause: "Request body is missing required 'question' field",
      fix: "Ensure JSON body includes { \"question\": \"your question here\" }",
    },
    {
      error: "RuntimeError: no running event loop",
      cause: "Mixing sync and async incorrectly",
      fix: "Use async def for route handlers and await chain.ainvoke()",
    },
  ],
  resources: [
    { title: "FastAPI Official Docs", url: "https://fastapi.tiangolo.com" },
    { title: "LangChain LCEL Docs", url: "https://python.langchain.com/docs/expression_language/" },
    { title: "OpenAI API Reference", url: "https://platform.openai.com/docs/api-reference" },
  ],
};
