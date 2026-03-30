"""Part 4 — CLI script: ingest all sample hospital documents into Qdrant."""

import asyncio
from pathlib import Path
from langchain_core.documents import Document
from langchain_qdrant import QdrantVectorStore

from part_04_rag_qdrant.data.documents.sample_docs import ALL_DOCUMENTS
from part_04_rag_qdrant.ingestion.chunker import chunk_documents
from part_04_rag_qdrant.ingestion.embedder import get_embeddings
from part_04_rag_qdrant.ingestion.ingestor import get_qdrant_client, ensure_collection
from shared.config import get_settings
from shared.logger import logger


def ingest_sample_documents() -> None:
    settings = get_settings()
    client = get_qdrant_client()
    embeddings = get_embeddings()

    ensure_collection(client, settings.qdrant_collection, vector_size=1536)

    all_docs: list[Document] = []
    for filename, (content, department, doc_type) in ALL_DOCUMENTS.items():
        doc = Document(
            page_content=content,
            metadata={
                "filename": filename,
                "department": department,
                "doc_type": doc_type,
                "source": f"data/documents/{filename}",
            },
        )
        all_docs.append(doc)

    chunks = chunk_documents(all_docs, chunk_size=800, chunk_overlap=150)
    logger.info(f"Total chunks to ingest: {len(chunks)}")

    vector_store = QdrantVectorStore(
        client=client,
        collection_name=settings.qdrant_collection,
        embedding=embeddings,
    )
    vector_store.add_documents(chunks)
    logger.info(f"Successfully ingested {len(chunks)} chunks from {len(ALL_DOCUMENTS)} documents")
    logger.info(f"Collection: {settings.qdrant_collection}")


if __name__ == "__main__":
    ingest_sample_documents()
