"""Part 4 — RAG chain built with LCEL."""

from operator import itemgetter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_openai import ChatOpenAI

from part_04_rag_qdrant.rag.prompts import RAG_PROMPT
from part_04_rag_qdrant.retrieval.retriever import get_retriever
from shared.config import get_settings


def _format_docs(docs) -> str:
    """Format retrieved documents into a context string."""
    parts = []
    for i, doc in enumerate(docs, 1):
        source = doc.metadata.get("filename", "Unknown")
        dept = doc.metadata.get("department", "")
        header = f"[Document {i}] Source: {source}"
        if dept:
            header += f" | Department: {dept}"
        parts.append(f"{header}\n{doc.page_content}")
    return "\n\n---\n\n".join(parts)


def build_rag_chain(
    k: int = 5,
    department: str | None = None,
    doc_type: str | None = None,
):
    """
    Build a RAG chain using LCEL (LangChain Expression Language).

    Returns a chain that accepts {"question": str} and returns an answer string.
    """
    settings = get_settings()
    llm = ChatOpenAI(
        model=settings.llm_model,
        openai_api_key=settings.openai_api_key,
        temperature=0.0,  # Factual — low temperature
    )
    retriever = get_retriever(k=k, department=department, doc_type=doc_type)

    chain = (
        {
            "context": retriever | RunnableLambda(_format_docs),
            "question": RunnablePassthrough(),
        }
        | RAG_PROMPT
        | llm
        | StrOutputParser()
    )
    return chain


def build_rag_chain_with_sources(
    k: int = 5,
    department: str | None = None,
):
    """
    RAG chain that returns both answer and source documents.

    Returns: {"answer": str, "sources": list[Document]}
    """
    settings = get_settings()
    llm = ChatOpenAI(
        model=settings.llm_model,
        openai_api_key=settings.openai_api_key,
        temperature=0.0,
    )
    retriever = get_retriever(k=k, department=department)

    def _extract_sources(inputs: dict) -> dict:
        docs = inputs["docs"]
        return {
            "answer": inputs["answer"],
            "sources": [
                {"filename": d.metadata.get("filename", ""), "snippet": d.page_content[:200]}
                for d in docs
            ],
        }

    chain = (
        RunnablePassthrough.assign(docs=retriever)
        | RunnablePassthrough.assign(
            context=lambda x: _format_docs(x["docs"]),
        )
        | RunnablePassthrough.assign(
            answer=RAG_PROMPT | llm | StrOutputParser()
        )
        | RunnableLambda(_extract_sources)
    )
    return chain
