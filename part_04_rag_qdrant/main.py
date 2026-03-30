"""Part 4 — FastAPI RAG endpoints."""

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field

from part_04_rag_qdrant.rag.chain import build_rag_chain, build_rag_chain_with_sources
from part_04_rag_qdrant.retrieval.retriever import get_vector_store
from shared.config import get_settings
from shared.logger import logger

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Part 4 — RAG + Qdrant app starting")
    yield
    logger.info("Part 4 shutting down")


app = FastAPI(
    title="Hospital AI Platform — Part 4: RAG + Qdrant",
    description="Retrieval-Augmented Generation over hospital documents.",
    version="1.0.0",
    lifespan=lifespan,
)


class SearchRequest(BaseModel):
    query: str = Field(min_length=3, max_length=500)
    k: int = Field(default=5, ge=1, le=20)
    department: str | None = None
    doc_type: str | None = None


class RAGRequest(BaseModel):
    question: str = Field(min_length=5, max_length=1000)
    department: str | None = None
    doc_type: str | None = None
    k: int = Field(default=5, ge=1, le=10)
    include_sources: bool = True


@app.post("/search")
async def semantic_search(request: SearchRequest):
    """Semantic similarity search over hospital documents."""
    try:
        store = get_vector_store()
        results = store.similarity_search_with_score(
            request.query,
            k=request.k,
        )
        return {
            "query": request.query,
            "results": [
                {
                    "content": doc.page_content,
                    "score": float(score),
                    "metadata": doc.metadata,
                }
                for doc, score in results
            ],
        }
    except Exception as exc:
        logger.error(f"Search failed: {exc}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Search service unavailable — is Qdrant running?",
        ) from exc


@app.post("/rag/ask")
async def rag_ask(request: RAGRequest):
    """Answer a question using RAG over hospital documents."""
    try:
        if request.include_sources:
            chain = build_rag_chain_with_sources(k=request.k, department=request.department)
            result = await chain.ainvoke(request.question)
            return result
        else:
            chain = build_rag_chain(
                k=request.k,
                department=request.department,
                doc_type=request.doc_type,
            )
            answer = await chain.ainvoke(request.question)
            return {"answer": answer}
    except Exception as exc:
        logger.error(f"RAG chain failed: {exc}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="RAG service unavailable",
        ) from exc


@app.get("/health")
async def health():
    try:
        from part_04_rag_qdrant.retrieval.qdrant_client import get_client
        client = get_client()
        collections = [c.name for c in client.get_collections().collections]
        return {
            "status": "healthy",
            "qdrant": "connected",
            "collections": collections,
        }
    except Exception as exc:
        return {
            "status": "degraded",
            "qdrant": "unavailable",
            "error": str(exc),
        }
