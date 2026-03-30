import type { PlaygroundConfig } from "../../types";
export const pg09: PlaygroundConfig = {
  partId: "09",
  endpoints: [
    { id: "start-prescription", method: "POST", path: "/workflow/prescription/start", description: "Start prescription approval workflow", exampleBody: { patient_id: "P001", doctor_id: "D001", drug_name: "Warfarin", dosage: "5mg daily", duration_days: 30, indication: "Atrial fibrillation" } },
    { id: "start-billing", method: "POST", path: "/workflow/billing/start", description: "Start billing review workflow", exampleBody: { patient_id: "P001", invoice_id: "INV-2026-001", amount: 8500.00, items: [{ description: "ICU Day 1", cost: 5000 }, { description: "Surgery", cost: 3500 }] } },
    { id: "start-discharge", method: "POST", path: "/workflow/discharge/start", description: "Initiate 3-step discharge sign-off", exampleBody: { patient_id: "P001", ward: "Cardiology-3B", primary_doctor: "Dr. Sarah Chen" } },
    { id: "resolve-approval", method: "POST", path: "/approvals/{approval_id}/resolve", description: "Approve or reject a pending item", pathParams: [{ name: "approval_id", example: "apr_abc123" }], exampleBody: { approved: true, reviewer_id: "DR001", notes: "Reviewed and approved. Monitor INR weekly." } },
    { id: "pending-approvals", method: "GET", path: "/approvals/pending", description: "List all pending approvals", exampleBody: null },
  ],
};
