import type { PlaygroundConfig } from "../../types";
export const pg10: PlaygroundConfig = {
  partId: "10",
  endpoints: [
    { id: "stream-chat", method: "POST", path: "/stream/chat", description: "SSE streaming chat — tokens appear live", exampleBody: { message: "Explain the difference between a stroke and a TIA in simple terms", session_id: "sess_stream_001" }, streaming: true },
    { id: "demo", method: "GET", path: "/demo", description: "Open the interactive streaming HTML demo", exampleBody: null },
  ],
};
