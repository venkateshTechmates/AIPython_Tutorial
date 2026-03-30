import type { PlaygroundConfig } from "../../types";
export const pg03: PlaygroundConfig = {
  partId: "03",
  endpoints: [
    { id: "create-patient", method: "POST", path: "/patients", description: "Create new patient", exampleBody: { name: "John Doe", date_of_birth: "1990-03-20", blood_type: "O+", email: "john.doe@email.com", phone: "+1-555-0101" } },
    { id: "get-patient", method: "GET", path: "/patients/{patient_id}", description: "Get patient by ID", pathParams: [{ name: "patient_id", example: "P001" }], exampleBody: null },
    { id: "list-patients", method: "GET", path: "/patients", description: "List patients with pagination", queryParams: [{ name: "page", example: "1" }, { name: "size", example: "10" }], exampleBody: null },
    { id: "update-patient", method: "PUT", path: "/patients/{patient_id}", description: "Update patient record", pathParams: [{ name: "patient_id", example: "P001" }], exampleBody: { phone: "+1-555-9999", email: "new.email@example.com" } },
    { id: "create-appointment", method: "POST", path: "/appointments", description: "Schedule appointment", exampleBody: { patient_id: "P001", doctor_id: "D001", scheduled_at: "2026-04-20T14:00:00", notes: "Follow-up on blood test results" } },
  ],
};
