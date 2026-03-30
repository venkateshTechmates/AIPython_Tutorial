"""Part 8 — Semantic memory: embedding patient summaries for retrieval-augmented recall."""

from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

# In-memory vector store for demo (swap for Qdrant in production)
from langchain_community.vectorstores import FAISS

_embeddings = None
_store: FAISS | None = None
_initialized = False


def _get_embeddings() -> OpenAIEmbeddings:
    global _embeddings
    if _embeddings is None:
        _embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    return _embeddings


def initialize_store(texts: list[str] | None = None) -> None:
    """Bootstrap the in-memory FAISS store, optionally with seed texts."""
    global _store, _initialized
    emb = _get_embeddings()
    seed = texts or ["Hospital AI semantic memory initialized."]
    _store = FAISS.from_texts(seed, emb)
    _initialized = True


def add_patient_summary(patient_id: str, summary: str, metadata: dict | None = None) -> None:
    """Embed and store a clinical summary associated with a patient."""
    global _store, _initialized
    if not _initialized:
        initialize_store()

    meta = {"patient_id": patient_id, **(metadata or {})}
    doc = Document(page_content=summary, metadata=meta)
    emb = _get_embeddings()
    _store.add_documents([doc])  # type: ignore[union-attr]


def search_patient_memories(query: str, patient_id: str | None = None, k: int = 3) -> list[dict]:
    """Semantic search over stored patient summaries.

    If *patient_id* is provided, results are filtered to that patient.
    """
    if not _initialized or _store is None:
        return []

    results = _store.similarity_search_with_score(query, k=k * 3 if patient_id else k)
    output = []
    for doc, score in results:
        if patient_id and doc.metadata.get("patient_id") != patient_id:
            continue
        output.append({
            "content": doc.page_content,
            "metadata": doc.metadata,
            "similarity_score": round(float(score), 4),
        })
        if len(output) >= k:
            break
    return output
