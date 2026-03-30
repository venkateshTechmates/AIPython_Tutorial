"""Part 1 — Medical query classification endpoint."""

import json
from fastapi import APIRouter, HTTPException, status
from langchain_core.output_parsers import StrOutputParser

from part_01_foundations.llm import get_llm
from part_01_foundations.prompts import CLASSIFY_PROMPT
from part_01_foundations.schemas import ClassifyRequest, ClassifyResponse, QueryType
from shared.logger import logger

router = APIRouter(prefix="/classify", tags=["Classify"])


@router.post("/", response_model=ClassifyResponse)
async def classify_query(request: ClassifyRequest) -> ClassifyResponse:
    """Classify a medical query into a routing category."""
    try:
        llm = get_llm()
        chain = CLASSIFY_PROMPT | llm | StrOutputParser()
        raw = await chain.ainvoke({"query": request.query})

        # Parse JSON response from LLM
        data = json.loads(raw.strip())
        return ClassifyResponse(
            query_type=QueryType(data["query_type"]),
            confidence=float(data["confidence"]),
            reasoning=data["reasoning"],
        )

    except json.JSONDecodeError as exc:
        logger.warning(f"LLM returned non-JSON classification: {exc}")
        # Graceful fallback
        return ClassifyResponse(
            query_type=QueryType.GENERAL,
            confidence=0.0,
            reasoning="Classification failed — defaulting to general",
        )
    except Exception as exc:
        logger.error(f"Classification failed: {exc}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Classification service temporarily unavailable",
        ) from exc
