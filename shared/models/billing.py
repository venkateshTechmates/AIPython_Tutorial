"""Billing domain model."""

from datetime import date, datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field, computed_field, model_validator


class BillingStatus(str, Enum):
    DRAFT = "draft"
    SENT = "sent"
    PARTIALLY_PAID = "partially_paid"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class BillingCategory(str, Enum):
    CONSULTATION = "consultation"
    PROCEDURE = "procedure"
    MEDICATION = "medication"
    LAB_TEST = "lab_test"
    IMAGING = "imaging"
    ROOM_CHARGES = "room_charges"
    NURSING_CARE = "nursing_care"
    EQUIPMENT = "equipment"
    OTHER = "other"


class BillingItem(BaseModel):
    description: str = Field(min_length=2, max_length=300)
    category: BillingCategory
    quantity: float = Field(gt=0)
    unit_price: float = Field(ge=0)
    discount_percent: float = Field(default=0.0, ge=0.0, le=100.0)
    cpt_code: str | None = Field(default=None, description="Current Procedural Terminology code")

    @computed_field
    @property
    def subtotal(self) -> float:
        gross = self.quantity * self.unit_price
        return round(gross * (1 - self.discount_percent / 100), 2)


class InvoiceBase(BaseModel):
    patient_id: int
    appointment_id: int | None = None
    items: list[BillingItem] = Field(min_length=1)
    issue_date: date
    due_date: date
    tax_percent: float = Field(default=0.0, ge=0.0, le=50.0)
    insurance_coverage_amount: float = Field(default=0.0, ge=0.0)
    notes: str | None = None

    @model_validator(mode="after")
    def validate_due_date(self) -> "InvoiceBase":
        if self.due_date < self.issue_date:
            raise ValueError("Due date cannot be before issue date")
        return self

    @computed_field
    @property
    def subtotal(self) -> float:
        return round(sum(item.subtotal for item in self.items), 2)

    @computed_field
    @property
    def tax_amount(self) -> float:
        return round(self.subtotal * self.tax_percent / 100, 2)

    @computed_field
    @property
    def total_amount(self) -> float:
        return round(self.subtotal + self.tax_amount, 2)

    @computed_field
    @property
    def patient_responsibility(self) -> float:
        return round(max(0.0, self.total_amount - self.insurance_coverage_amount), 2)

    model_config = ConfigDict(populate_by_name=True)


class InvoiceCreate(InvoiceBase):
    pass


class Invoice(InvoiceBase):
    id: int
    invoice_number: str  # e.g. "INV-00321"
    status: BillingStatus = BillingStatus.DRAFT
    paid_amount: float = 0.0
    paid_at: datetime | None = None
    created_at: datetime
    updated_at: datetime

    @computed_field
    @property
    def balance_due(self) -> float:
        return round(max(0.0, self.patient_responsibility - self.paid_amount), 2)

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
