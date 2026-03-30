import type { PlaygroundConfig } from "../../types";
export const pg01: PlaygroundConfig = {
  partId: "01",
  endpoints: [
    { id: "health", method: "GET", path: "/health", description: "Check server health", exampleBody: null },
    { id: "ask", method: "POST", path: "/ask", description: "Ask a hospital question", exampleBody: { question: "What are the ICU visiting hours?", patient_id: "P001" } },
    { id: "summarise", method: "POST", path: "/summarise", description: "Summarise clinical notes", exampleBody: { clinical_notes: "Patient presented with fever 38.5°C, cough for 3 days. BP 120/80. SpO2 98% on room air. CXR clear. Impression: viral URTI.", max_sentences: 2 } },
    { id: "classify", method: "POST", path: "/classify", description: "Classify query intent", exampleBody: { query: "I need to book an appointment with a cardiologist" } },
  ],
};
