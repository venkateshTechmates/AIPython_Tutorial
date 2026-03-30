import type { PlaygroundConfig } from "../../types";
export const pg05: PlaygroundConfig = {
  partId: "05",
  endpoints: [
    { id: "start-triage", method: "POST", path: "/triage", description: "Start a new triage session", exampleBody: { patient_id: "P001", chief_complaint: "Chest pain radiating to left arm, started 2 hours ago" } },
    { id: "send-message", method: "POST", path: "/triage/{session_id}/message", description: "Continue triage conversation", pathParams: [{ name: "session_id", example: "sess_abc123" }], exampleBody: { message: "The pain is 8/10 and I feel nauseous and sweaty" } },
    { id: "get-state", method: "GET", path: "/triage/{session_id}/state", description: "Get current triage state", pathParams: [{ name: "session_id", example: "sess_abc123" }], exampleBody: null },
    { id: "get-history", method: "GET", path: "/triage/{session_id}/history", description: "Get full conversation history", pathParams: [{ name: "session_id", example: "sess_abc123" }], exampleBody: null },
  ],
};
