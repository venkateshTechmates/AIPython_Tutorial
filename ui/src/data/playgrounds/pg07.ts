import type { PlaygroundConfig } from "../../types";
export const pg07: PlaygroundConfig = {
  partId: "07",
  endpoints: [
    { id: "agent-chat", method: "POST", path: "/agent/chat", description: "Chat with the 13-tool ReAct agent", exampleBody: { message: "Look up patient P001 and check if they have any appointments this week", session_id: "sess_tools_001" } },
    { id: "list-tools", method: "GET", path: "/tools", description: "List all 13 available tools with schemas", exampleBody: null },
  ],
};
