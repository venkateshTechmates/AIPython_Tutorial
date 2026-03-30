import type { PlaygroundConfig } from "../../types";
export const pg12: PlaygroundConfig = {
  partId: "12",
  endpoints: [
    { id: "observe-chat", method: "POST", path: "/observe/chat", description: "Chat with LangSmith tracing enabled", exampleBody: { message: "List all doctors in cardiology", session_id: "sess_obs_001", patient_id: "P001" } },
    { id: "metrics", method: "GET", path: "/metrics", description: "Get full metrics snapshot", exampleBody: null },
  ],
};
