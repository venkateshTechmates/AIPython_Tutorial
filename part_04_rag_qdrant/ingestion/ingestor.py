"""Part 4 — Full ingestion pipeline orchestrator."""

from pathlib import Path
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from part_04_rag_qdrant.ingestion.loader import load_directory, load_document
from part_04_rag_qdrant.ingestion.chunker import chunk_documents
from part_04_rag_qdrant.ingestion.embedder import get_embeddings
from shared.config import get_settings
from shared.logger import logger


def get_qdrant_client() -> QdrantClient:
    settings = get_settings()
    return QdrantClient(
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key or None,
    )


def ensure_collection(client: QdrantClient, collection_name: str, vector_size: int = 1536) -> None:
    """Create Qdrant collection if it doesn't exist."""
    existing = [c.name for c in client.get_collections().collections]
    if collection_name not in existing:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )
        logger.info(f"Created Qdrant collection: {collection_name}")
    else:
        logger.info(f"Using existing Qdrant collection: {collection_name}")


def ingest_documents(
    source_path: str | Path,
    department: str | None = None,
    doc_type: str | None = None,
    chunk_size: int = 800,
    chunk_overlap: int = 150,
) -> int:
    """
    Full pipeline: load → chunk → embed → store in Qdrant.
    Returns the number of chunks ingested.
    """
    settings = get_settings()
    path = Path(source_path)

    # Load
    if path.is_dir():
        docs = load_directory(path, department=department, doc_type=doc_type)
    else:
        meta = {}
        if department:
            meta["department"] = department
        if doc_type:
            meta["doc_type"] = doc_type
        docs = load_document(path, metadata=meta)

    if not docs:
        logger.warning(f"No documents found at {source_path}")
        return 0

    # Chunk
    chunks = chunk_documents(docs, chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    # Embed + Store
    client = get_qdrant_client()
    embeddings = get_embeddings()

    # text-embedding-3-small = 1536 dims
    ensure_collection(client, settings.qdrant_collection, vector_size=1536)

    vector_store = QdrantVectorStore(
        client=client,
        collection_name=settings.qdrant_collection,
        embedding=embeddings,
    )
    vector_store.add_documents(chunks)
    logger.info(f"Ingested {len(chunks)} chunks into Qdrant collection '{settings.qdrant_collection}'")
    return len(chunks)
