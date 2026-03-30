"""Part 4 — Document loaders: PDF, text, and markdown."""

from pathlib import Path
from langchain_core.documents import Document
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredMarkdownLoader,
)
from shared.logger import logger


def load_document(file_path: str | Path, metadata: dict | None = None) -> list[Document]:
    """Load a document from file, return list of LangChain Documents."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Document not found: {file_path}")

    extra_meta = metadata or {}
    extra_meta["source"] = str(path)
    extra_meta["filename"] = path.name

    suffix = path.suffix.lower()
    if suffix == ".pdf":
        loader = PyPDFLoader(str(path))
    elif suffix in (".txt", ".text"):
        loader = TextLoader(str(path), encoding="utf-8")
    elif suffix in (".md", ".markdown"):
        loader = UnstructuredMarkdownLoader(str(path))
    else:
        raise ValueError(f"Unsupported document type: {suffix}")

    docs = loader.load()
    for doc in docs:
        doc.metadata.update(extra_meta)
    logger.info(f"Loaded {len(docs)} page(s) from {path.name}")
    return docs


def load_directory(
    directory: str | Path,
    department: str | None = None,
    doc_type: str | None = None,
) -> list[Document]:
    """Recursively load all supported documents from a directory."""
    dir_path = Path(directory)
    all_docs: list[Document] = []
    supported = {".pdf", ".txt", ".text", ".md", ".markdown"}

    for file_path in dir_path.rglob("*"):
        if file_path.suffix.lower() in supported:
            meta = {}
            if department:
                meta["department"] = department
            if doc_type:
                meta["doc_type"] = doc_type
            try:
                docs = load_document(file_path, metadata=meta)
                all_docs.extend(docs)
            except Exception as e:
                logger.warning(f"Failed to load {file_path}: {e}")

    logger.info(f"Total documents loaded from {dir_path}: {len(all_docs)}")
    return all_docs
