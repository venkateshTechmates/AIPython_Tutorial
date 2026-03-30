"""Part 1 — Ask and Summarize endpoints."""

import json
from fastapi import APIRouter, HTTPException, status
from langchain_core.output_parsers import StrOutputParser

from part_01_foundations.llm import get_llm
from part_01_foundations.prompts import ASK_PROMPT, ASK_WITH_CONTEXT_PROMPT, SUMMARIZE_PROMPT
from part_01_foundations.schemas import (
    AskRequest,
    AskResponse,
    SummarizeRequest,
    SummarizeResponse,
)
from shared.config import get_settings
from shared.logger import logger

router = APIRouter(prefix="/ask", tags=["Ask"])
settings = get_settings()


@router.post("/", response_model=AskResponse)
async def ask_question(request: AskRequest) -> AskResponse:
    """Send a question to the LLM and receive an answer."""
    try:
        llm = get_llm()
        prompt = ASK_WITH_CONTEXT_PROMPT if request.context else ASK_PROMPT

        chain = prompt | llm | StrOutputParser()

        if request.context:
            answer = await chain.ainvoke(
                {"question": request.question, "context": request.context}
            )
        else:
            answer = await chain.ainvoke({"question": request.question})

        return AskResponse(answer=answer, model_used=settings.llm_model)

    except Exception as exc:
        logger.error(f"LLM call failed: {exc}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="LLM service temporarily unavailable",
        ) from exc


@router.post("/summarize", response_model=SummarizeResponse)
async def summarize_notes(request: SummarizeRequest) -> SummarizeResponse:
    """Summarize patient clinical notes."""
    try:
        llm = get_llm()
        chain = SUMMARIZE_PROMPT | llm | StrOutputParser()

        summary = await chain.ainvoke(
            {
                "patient_notes": request.patient_notes,
                "max_sentences": request.max_sentences,
            }
        )

        return SummarizeResponse(
            summary=summary,
            original_length=len(request.patient_notes),
            summary_length=len(summary),
        )

    except Exception as exc:
        logger.error(f"Summarization failed: {exc}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Summarization service temporarily unavailable",
        ) from exc
