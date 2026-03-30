import type { PlaygroundConfig } from "../../types";
export const pg08: PlaygroundConfig = {
  partId: "08",
  endpoints: [
    { id: "memory-chat", method: "POST", path: "/memory/chat", description: "Chat with full memory-aware agent", exampleBody: { message: "What medications is patient P001 currently taking?", patient_id: "P001", session_id: "sess_mem_001" } },
    { id: "save-memory", method: "POST", path: "/memory/save", description: "Persist a patient memory fact", exampleBody: { patient_id: "P001", category: "preferences", key: "language", value: "English" } },
    { id: "get-memory", method: "GET", path: "/memory/{patient_id}", description: "Retrieve all memory for a patient", pathParams: [{ name: "patient_id", example: "P001" }], exampleBody: null },
    { id: "add-summary", method: "POST", path: "/memory/summary", description: "Add a semantic summary to vector memory", exampleBody: { patient_id: "P001", summary: "Patient visited on 2026-03-15 for follow-up on hypertension. BP 135/85. Medication adjusted to Lisinopril 10mg." } },
    { id: "recall", method: "GET", path: "/memory/{patient_id}/recall", description: "Semantic recall by query", pathParams: [{ name: "patient_id", example: "P001" }], queryParams: [{ name: "query", example: "blood pressure history" }], exampleBody: null },
    { id: "sessions", method: "GET", path: "/sessions", description: "List active sessions", exampleBody: null },
  ],
};
