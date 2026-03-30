"""Part 4 — LangChain retriever wrapper over Qdrant."""

from functools import lru_cache
from langchain_qdrant import QdrantVectorStore
from langchain_core.vectorstores import VectorStoreRetriever
from qdrant_client.models import Filter, FieldCondition, MatchValue

from part_04_rag_qdrant.ingestion.embedder import get_embeddings
from part_04_rag_qdrant.retrieval.qdrant_client import get_client
from shared.config import get_settings


def get_vector_store() -> QdrantVectorStore:
    settings = get_settings()
    return QdrantVectorStore(
        client=get_client(),
        collection_name=settings.qdrant_collection,
        embedding=get_embeddings(),
    )


def get_retriever(
    k: int = 5,
    department: str | None = None,
    doc_type: str | None = None,
) -> VectorStoreRetriever:
    """
    Build a retriever with optional metadata filters.

    Args:
        k: Number of documents to retrieve
        department: Filter by department metadata field
        doc_type: Filter by doc_type metadata field
    """
    store = get_vector_store()

    search_kwargs: dict = {"k": k}

    # Build Qdrant filter for metadata fields
    conditions = []
    if department:
        conditions.append(
            FieldCondition(key="metadata.department", match=MatchValue(value=department))
        )
    if doc_type:
        conditions.append(
            FieldCondition(key="metadata.doc_type", match=MatchValue(value=doc_type))
        )

    if conditions:
        search_kwargs["filter"] = Filter(must=conditions)

    return store.as_retriever(search_type="similarity", search_kwargs=search_kwargs)
