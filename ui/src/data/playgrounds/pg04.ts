import type { PlaygroundConfig } from "../../types";
export const pg04: PlaygroundConfig = {
  partId: "04",
  endpoints: [
    { id: "ingest", method: "POST", path: "/ingest", description: "Ingest documents into Qdrant", exampleBody: { documents: [{ content: "ICU visiting hours are 10am to 8pm daily. Maximum 2 visitors at a time. Children under 12 are not permitted.", source: "hospital_policy.pdf", page: 1 }], collection: "hospital_docs" } },
    { id: "search", method: "POST", path: "/search", description: "Semantic similarity search", exampleBody: { query: "What are visiting hour restrictions?", collection: "hospital_docs", top_k: 3 } },
    { id: "rag-ask", method: "POST", path: "/rag/ask", description: "RAG-powered Q&A with citations", exampleBody: { question: "Can children visit ICU patients?", collection: "hospital_docs", include_sources: true } },
    { id: "collections", method: "GET", path: "/collections", description: "List Qdrant collections and stats", exampleBody: null },
  ],
};
