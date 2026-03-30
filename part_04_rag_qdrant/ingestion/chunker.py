"""Part 4 — Text splitting strategies for RAG chunking."""

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
from shared.logger import logger


def chunk_documents(
    documents: list[Document],
    chunk_size: int = 800,
    chunk_overlap: int = 150,
) -> list[Document]:
    """Split documents into overlapping chunks using recursive character splitting."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", "! ", "? ", " ", ""],
        length_function=len,
        add_start_index=True,
    )
    chunks = splitter.split_documents(documents)
    logger.info(f"Chunked {len(documents)} documents → {len(chunks)} chunks")
    return chunks


def chunk_markdown(documents: list[Document]) -> list[Document]:
    """Split markdown documents by header hierarchy, then by size."""
    headers_to_split_on = [
        ("#", "header_1"),
        ("##", "header_2"),
        ("###", "header_3"),
    ]
    header_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on,
        strip_headers=False,
    )
    char_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)

    all_chunks: list[Document] = []
    for doc in documents:
        try:
            header_chunks = header_splitter.split_text(doc.page_content)
            fine_chunks = char_splitter.split_documents(header_chunks)
            for chunk in fine_chunks:
                chunk.metadata.update(doc.metadata)
            all_chunks.extend(fine_chunks)
        except Exception:
            # Fallback to standard chunking
            all_chunks.extend(char_splitter.split_documents([doc]))

    return all_chunks
