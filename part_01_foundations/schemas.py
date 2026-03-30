"""Part 1 — Pydantic request/response schemas."""

from enum import Enum
from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(min_length=3, max_length=2000)
    context: str | None = Field(default=None, max_length=5000)

    model_config = {
        "json_schema_extra": {
            "examples": [{"question": "What are the symptoms of appendicitis?"}]
        }
    }


class AskResponse(BaseModel):
    answer: str
    model_used: str
    tokens_used: int | None = None


class SummarizeRequest(BaseModel):
    patient_notes: str = Field(min_length=10, max_length=10000)
    max_sentences: int = Field(default=3, ge=1, le=10)


class SummarizeResponse(BaseModel):
    summary: str
    original_length: int
    summary_length: int


class QueryType(str, Enum):
    TRIAGE = "triage"
    BILLING = "billing"
    APPOINTMENT = "appointment"
    MEDICATION = "medication"
    GENERAL = "general"


class ClassifyRequest(BaseModel):
    query: str = Field(min_length=3, max_length=1000)


class ClassifyResponse(BaseModel):
    query_type: QueryType
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str


class HealthResponse(BaseModel):
    status: str
    llm_model: str
    environment: str
    version: str = "1.0.0"
