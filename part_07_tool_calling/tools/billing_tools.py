"""Part 7 — Billing and invoice tools."""

from langchain_core.tools import tool
from pydantic import BaseModel, Field


class GetInvoiceInput(BaseModel):
    invoice_id: str = Field(description="Invoice ID (e.g. 'INV-00042')")


class CalculateBillInput(BaseModel):
    appointment_id: str = Field(description="Appointment number or ID")
    include_medications: bool = Field(default=False, description="Include medication costs")


class ApplyDiscountInput(BaseModel):
    invoice_id: str = Field(description="Invoice ID to apply discount to")
    discount_percent: float = Field(description="Discount percentage (0–100)", ge=0, le=100)
    reason: str = Field(description="Reason for the discount (insurance, hardship, etc.)")


_MOCK_INVOICES: dict[str, dict] = {
    "INV-00001": {
        "invoice_id": "INV-00001",
        "patient_id": 1,
        "patient_name": "John Smith",
        "items": [
            {"description": "Cardiology Consultation", "quantity": 1, "unit_price": 300.0},
            {"description": "EKG", "quantity": 1, "unit_price": 85.0},
        ],
        "subtotal": 385.0,
        "tax_rate": 0.0,
        "tax_amount": 0.0,
        "total": 385.0,
        "insurance_coverage": 308.0,
        "patient_responsibility": 77.0,
        "status": "pending",
        "due_date": "2025-08-15",
    },
    "INV-00002": {
        "invoice_id": "INV-00002",
        "patient_id": 2,
        "patient_name": "Maria Garcia",
        "items": [
            {"description": "General Practice Visit", "quantity": 1, "unit_price": 150.0},
            {"description": "Lab Work - CBC", "quantity": 1, "unit_price": 45.0},
        ],
        "subtotal": 195.0,
        "tax_rate": 0.0,
        "tax_amount": 0.0,
        "total": 195.0,
        "insurance_coverage": 156.0,
        "patient_responsibility": 39.0,
        "status": "paid",
        "due_date": "2025-07-30",
    },
}


@tool("get_invoice_by_id", args_schema=GetInvoiceInput)
async def get_invoice_by_id(invoice_id: str) -> dict:
    """Retrieve a billing invoice by its ID, including itemized charges and insurance coverage."""
    invoice = _MOCK_INVOICES.get(invoice_id)
    if not invoice:
        return {"error": f"Invoice '{invoice_id}' not found."}
    return invoice


@tool("calculate_bill", args_schema=CalculateBillInput)
async def calculate_bill(appointment_id: str, include_medications: bool = False) -> dict:
    """Calculate the estimated bill for an appointment, optionally including medications."""
    base_charges = {
        "consultation_fee": 250.0,
        "facility_fee": 50.0,
    }
    if include_medications:
        base_charges["medications"] = 75.0

    subtotal = sum(base_charges.values())
    insurance_coverage = subtotal * 0.80
    patient_responsibility = subtotal - insurance_coverage

    return {
        "appointment_id": appointment_id,
        "charges": base_charges,
        "subtotal": subtotal,
        "insurance_coverage": round(insurance_coverage, 2),
        "patient_responsibility": round(patient_responsibility, 2),
        "includes_medications": include_medications,
        "note": "Estimated charges — final bill may vary based on services rendered.",
    }


@tool("apply_discount", args_schema=ApplyDiscountInput)
async def apply_discount(invoice_id: str, discount_percent: float, reason: str) -> dict:
    """Apply a discount to an existing invoice for insurance adjustments or financial hardship."""
    invoice = _MOCK_INVOICES.get(invoice_id)
    if not invoice:
        return {"error": f"Invoice '{invoice_id}' not found."}

    original_total = invoice["total"]
    discount_amount = round(original_total * (discount_percent / 100), 2)
    new_total = round(original_total - discount_amount, 2)
    new_patient_responsibility = round(new_total - invoice["insurance_coverage"], 2)

    return {
        "invoice_id": invoice_id,
        "original_total": original_total,
        "discount_percent": discount_percent,
        "discount_amount": discount_amount,
        "new_total": new_total,
        "new_patient_responsibility": max(new_patient_responsibility, 0.0),
        "reason": reason,
        "status": "discount_applied",
    }
