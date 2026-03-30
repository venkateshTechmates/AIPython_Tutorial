import type { PlaygroundConfig } from "../../types";
export const pg02: PlaygroundConfig = {
  partId: "02",
  endpoints: [
    { id: "validate-patient", method: "POST", path: "/patients/validate", description: "Validate a patient record", exampleBody: { name: "Jane Smith", date_of_birth: "1985-06-15", blood_type: "A+", email: "jane.smith@email.com", phone: "+1-555-0123" } },
    { id: "validate-appointment", method: "POST", path: "/appointments/validate", description: "Validate appointment data", exampleBody: { patient_id: "P001", doctor_id: "D001", scheduled_at: "2026-04-15T10:00:00", specialty: "cardiology" } },
    { id: "validate-billing", method: "POST", path: "/billing/validate", description: "Validate billing record", exampleBody: { patient_id: "P001", amount: 1500.00, insurance_covered: true, items: [{ description: "Consultation", cost: 500 }, { description: "Blood Test", cost: 1000 }] } },
    { id: "schema", method: "GET", path: "/schema/patient", description: "Get JSON Schema for Patient model", exampleBody: null },
  ],
};
