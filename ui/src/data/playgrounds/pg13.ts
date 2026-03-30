import type { PlaygroundConfig } from "../../types";
export const pg13: PlaygroundConfig = {
  partId: "13",
  endpoints: [
    { id: "health", method: "GET", path: "/health", description: "Production health check with version info", exampleBody: null },
  ],
};
