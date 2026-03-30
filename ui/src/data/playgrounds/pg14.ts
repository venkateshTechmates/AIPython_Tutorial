import type { PlaygroundConfig } from "../../types";
export const pg14: PlaygroundConfig = {
  partId: "14",
  endpoints: [
    { id: "platform-chat", method: "POST", path: "/platform/chat", description: "Full patient journey — auto-routes to emergency/tools/RAG", exampleBody: { message: "I have been experiencing chest tightness and shortness of breath for the past hour", patient_id: "P001", session_id: "sess_cap_001" } },
    { id: "platform-chat-stream", method: "POST", path: "/platform/chat", description: "Streaming platform chat (set stream: true)", exampleBody: { message: "What medications can interact with Warfarin?", patient_id: "P001", session_id: "sess_cap_002", stream: true }, streaming: true },
    { id: "save-memory", method: "POST", path: "/platform/memory", description: "Save a patient memory fact", exampleBody: { patient_id: "P001", key: "preferred_doctor", value: "Dr. Sarah Chen", category: "preferences" } },
    { id: "get-memory", method: "GET", path: "/platform/patient/{patient_id}/memory", description: "Get all memory for patient", pathParams: [{ name: "patient_id", example: "P001" }], exampleBody: null },
    { id: "health", method: "GET", path: "/health", description: "Platform health check", exampleBody: null },
  ],
};
