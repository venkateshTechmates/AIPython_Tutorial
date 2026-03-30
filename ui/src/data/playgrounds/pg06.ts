import type { PlaygroundConfig } from "../../types";
export const pg06: PlaygroundConfig = {
  partId: "06",
  endpoints: [
    { id: "supervisor-chat", method: "POST", path: "/supervisor/chat", description: "Submit query to supervisor — auto-routes to specialist", exampleBody: { message: "What is covered under my insurance plan?", session_id: "sess_001" } },
    { id: "list-agents", method: "GET", path: "/agents", description: "List all available specialised agents", exampleBody: null },
    { id: "session-history", method: "GET", path: "/supervisor/sessions/{session_id}", description: "Get session with agent routing history", pathParams: [{ name: "session_id", example: "sess_001" }], exampleBody: null },
  ],
};
