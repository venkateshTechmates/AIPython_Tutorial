import type { PartData } from "../../types";

export const part04: PartData = {
  id: "04",
  title: "RAG + Qdrant Vector Search",
  goal: "Build a Retrieval-Augmented Generation pipeline that answers questions from hospital policy documents.",
  phase: 2,
  phaseLabel: "RAG & First Agent",
  folder: "part_04_rag",
  estimatedHours: 5,
  difficulty: "intermediate",
  prerequisites: ["01", "02", "03"],
  unlocks: ["05"],
  whatYouBuild: [
    { label: "POST /ingest", description: "Ingest documents into Qdrant vector store" },
    { label: "POST /search", description: "Semantic similarity search over documents" },
    { label: "POST /rag/ask", description: "RAG-powered Q&A with source citations" },
    { label: "GET /collections", description: "List Qdrant collections and stats" },
  ],
  mermaidDiagram: `
flowchart TD
  subgraph Ingestion
    A[PDF / Text] --> B[RecursiveCharacterTextSplitter]
    B --> C[OpenAI Embeddings]
    C --> D[(Qdrant Vector DB)]
  end

  subgraph RAG Query
    E[User Question] --> F[Embed Question]
    F --> G[Similarity Search]
    G --> D
    D --> H[Top-K Chunks]
    H --> I[Stuffing Prompt]
    E --> I
    I --> J[GPT-4o]
    J --> K[Answer + Sources]
  end
  `,
  concepts: [
    {
      id: "embeddings",
      title: "Text Embeddings",
      explanation:
        "Embeddings convert text into high-dimensional vectors. Semantically similar text produces similar vectors. OpenAI's text-embedding-3-small produces 1536-dimension vectors.",
      code: {
        language: "python",
        filename: "rag/embeddings.py",
        snippet: `from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    dimensions=1536
)

# Generate embedding for a query
vector = await embeddings.aembed_query(
    "What are the ICU visiting hours?"
)
# Returns: list[float] of length 1536`,
      },
      glossaryTerms: ["Embedding", "Vector DB", "Semantic Search"],
    },
    {
      id: "qdrant-setup",
      title: "Qdrant Vector Store",
      explanation:
        "Qdrant stores vectors with metadata (payload). LangChain's QdrantVectorStore wraps Qdrant to handle embedding + storage automatically.",
      code: {
        language: "python",
        filename: "rag/vector_store.py",
        snippet: `from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

client = QdrantClient(url="http://localhost:6333")

# Create collection
client.create_collection(
    "hospital_docs",
    vectors_config=VectorParams(
        size=1536, distance=Distance.COSINE
    )
)

vector_store = QdrantVectorStore(
    client=client,
    collection_name="hospital_docs",
    embedding=embeddings
)`,
      },
      glossaryTerms: ["Qdrant", "Vector Store", "Cosine Similarity"],
    },
    {
      id: "rag-chain",
      title: "RAG Chain with Citations",
      explanation:
        "The RAG chain retrieves relevant chunks, stuffs them into the prompt, and returns both the answer and source documents for citation.",
      code: {
        language: "python",
        filename: "rag/pipeline.py",
        snippet: `from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

def format_docs(docs):
    return "\\n\\n".join(d.page_content for d in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | RAG_PROMPT
    | llm
    | StrOutputParser()
)

answer = await rag_chain.ainvoke("What is the visitor policy?")`,
      },
      glossaryTerms: ["RAG", "Retriever", "Context Stuffing"],
    },
  ],
  steps: [
    {
      number: 1,
      title: "Start Qdrant with Docker",
      description: "Run Qdrant locally via docker-compose.",
      code: {
        language: "bash",
        filename: "terminal",
        snippet: `docker run -p 6333:6333 qdrant/qdrant`,
      },
    },
    {
      number: 2,
      title: "Create the document ingestion pipeline",
      description: "Split documents, embed them, and store in Qdrant.",
    },
    {
      number: 3,
      title: "Build the retriever",
      description: "Configure max_marginal_relevance_search for diverse results.",
    },
    {
      number: 4,
      title: "Assemble the RAG chain",
      description: "Combine retriever + prompt + LLM + output parser.",
    },
    {
      number: 5,
      title: "Add source citations to response",
      description: "Return source document metadata (filename, page, score) alongside the answer.",
    },
  ],
  acceptanceCriteria: [
    { id: "ac1", text: "POST /ingest stores documents with metadata in Qdrant" },
    { id: "ac2", text: "POST /rag/ask returns relevant answers from ingested content" },
    { id: "ac3", text: "Response includes source_documents with filename and page" },
    { id: "ac4", text: "Semantic search finds conceptually related content" },
    { id: "ac5", text: "Unrelated questions return a graceful 'I don't know' response" },
  ],
  gotchas: [
    {
      error: "qdrant_client.http.exceptions.UnexpectedResponse: 404",
      cause: "Collection doesn't exist before first ingest",
      fix: "Call client.recreate_collection() in the lifespan startup to ensure the collection exists",
    },
    {
      error: "Empty retrieval results despite ingested content",
      cause: "Query embedding and document embeddings use different models",
      fix: "Ensure the same embeddings model is used for both ingestion and querying",
    },
  ],
  resources: [
    { title: "Qdrant Docs", url: "https://qdrant.tech/documentation/" },
    { title: "LangChain RAG Tutorial", url: "https://python.langchain.com/docs/tutorials/rag/" },
    { title: "OpenAI Embeddings", url: "https://platform.openai.com/docs/guides/embeddings" },
  ],
};
