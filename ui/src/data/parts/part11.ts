import type { PartData } from "../../types";

export const part11: PartData = {
  id: "11",
  title: "Testing Infrastructure",
  goal: "Build a comprehensive test suite: unit tests for nodes, integration tests for agent flows, and RAG quality evaluations.",
  phase: 4,
  phaseLabel: "Production Patterns",
  folder: "part_11_testing",
  estimatedHours: 4,
  difficulty: "intermediate",
  prerequisites: ["05", "06", "07", "08"],
  unlocks: ["12"],
  whatYouBuild: [
    { label: "pytest tests/unit/", description: "Run unit tests for nodes and validators" },
    { label: "pytest tests/integration/", description: "Run cross-part integration tests" },
    { label: "pytest tests/evaluation/", description: "Run RAG quality evaluations" },
  ],
  mermaidDiagram: `
flowchart TD
  subgraph Unit Tests
    A[test_nodes.py] --> B[Mock LLM]
    C[test_validators.py] --> D[Pydantic Models]
  end

  subgraph Integration Tests
    E[test_agent_flows.py] --> F[In-Memory SQLite]
    F --> G[Full Agent Graph]
  end

  subgraph Evaluation Tests
    H[test_rag_quality.py] --> I[Sample Queries]
    I --> J[RAG Pipeline]
    J --> K[Quality Assertions]
  end
  `,
  concepts: [
    {
      id: "mock-llm",
      title: "Mocking LLMs in Tests",
      explanation:
        "To test agent nodes without API calls, replace the real LLM with a MagicMock that returns a pre-defined AIMessage. This makes tests fast and deterministic.",
      code: {
        language: "python",
        filename: "tests/conftest.py",
        snippet: `import pytest
from unittest.mock import MagicMock
from langchain_core.messages import AIMessage

@pytest.fixture
def mock_llm():
    llm = MagicMock()
    llm.invoke.return_value = AIMessage(
        content="Mocked LLM response"
    )
    llm.bind_tools.return_value = llm
    return llm

@pytest.fixture
def async_mock_llm():
    llm = MagicMock()
    async def async_invoke(*args, **kwargs):
        return AIMessage(content="Async mocked response")
    llm.ainvoke = async_invoke
    llm.bind_tools.return_value = llm
    return llm`,
      },
      glossaryTerms: ["Mocking", "pytest", "Unit Test"],
    },
    {
      id: "node-testing",
      title: "Testing Individual Graph Nodes",
      explanation:
        "Test each LangGraph node in isolation by calling it directly with a crafted state dict. No graph compilation needed.",
      code: {
        language: "python",
        filename: "tests/unit/test_nodes.py",
        snippet: `@pytest.mark.asyncio
async def test_urgency_node_high_score(async_mock_llm):
    async_mock_llm.ainvoke = AsyncMock(return_value=AIMessage(
        content='{"urgency_score": 9, "label": "high"}'
    ))
    state = {
        "messages": [HumanMessage("severe chest pain")],
        "patient_id": "P001",
    }
    result = await urgency_check_node(state)
    assert result["urgency_score"] == 9
    assert result["urgency_label"] == "high"`,
      },
    },
    {
      id: "evaluation-tests",
      title: "RAG Quality Evaluation",
      explanation:
        "Evaluation tests use a labelled dataset of questions with expected intents and keywords. They verify the RAG pipeline answers correctly without calling real OpenAI.",
      code: {
        language: "python",
        filename: "tests/evaluation/test_rag_quality.py",
        snippet: `@pytest.mark.evaluation
@pytest.mark.parametrize("query,expected_intent", [
    ("What are ICU visiting hours?", "general_info"),
    ("I have chest pain", "emergency"),
    ("Book appointment cardiology", "appointment"),
])
def test_intent_classification(query, expected_intent, mock_llm):
    mock_llm.invoke.return_value = AIMessage(
        content=f'{{"intent": "{expected_intent}", "confidence": 0.9}}'
    )
    result = classify_intent_node(mock_llm)({"messages": [HumanMessage(query)]})
    assert result["intent"] == expected_intent`,
      },
    },
  ],
  steps: [
    { number: 1, title: "Set up pytest.ini and conftest.py", description: "Configure markers (unit, integration, evaluation) and shared fixtures." },
    { number: 2, title: "Write unit tests for LangGraph nodes", description: "Test each node in isolation with mock LLMs." },
    { number: 3, title: "Write Pydantic validator tests", description: "Test field validators, computed fields, and model validators." },
    { number: 4, title: "Write integration tests", description: "Full graph integration tests with in-memory SQLite." },
    { number: 5, title: "Write RAG evaluation tests", description: "Parametrize over sample_queries.json fixture." },
  ],
  acceptanceCriteria: [
    { id: "ac1", text: "pytest tests/unit/ passes with 100% success" },
    { id: "ac2", text: "All Pydantic validators have corresponding tests" },
    { id: "ac3", text: "Integration tests use no real API calls (autouse fixture blocks them)" },
    { id: "ac4", text: "Emergency queries always produce urgency response (safety check)" },
  ],
  gotchas: [
    {
      error: "ScopeMismatch: function-scoped fixture 'db' cannot use session-scoped",
      cause: "Mixing fixture scopes incorrectly",
      fix: "Match fixture scopes — use function scope for database fixtures to ensure isolation",
    },
    {
      error: "RuntimeWarning: coroutine 'xyz' was never awaited",
      cause: "Missing @pytest.mark.asyncio on async test function",
      fix: "Add asyncio_mode = auto in pytest.ini or mark each async test",
    },
  ],
  resources: [
    { title: "pytest docs", url: "https://docs.pytest.org/en/stable/" },
    { title: "pytest-asyncio", url: "https://pytest-asyncio.readthedocs.io" },
  ],
};
