"""Prescription domain model."""

from datetime import date, datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class FrequencyUnit(str, Enum):
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    AS_NEEDED = "as_needed"


class RouteOfAdministration(str, Enum):
    ORAL = "oral"
    INTRAVENOUS = "iv"
    INTRAMUSCULAR = "im"
    SUBCUTANEOUS = "subcutaneous"
    TOPICAL = "topical"
    INHALATION = "inhalation"
    SUBLINGUAL = "sublingual"
    RECTAL = "rectal"
    OPHTHALMIC = "ophthalmic"


class PrescriptionStatus(str, Enum):
    DRAFT = "draft"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    DISPENSED = "dispensed"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class MedicationItem(BaseModel):
    drug_name: str = Field(min_length=2, max_length=200)
    generic_name: str | None = None
    strength: str = Field(description="e.g. '500mg', '10mg/5ml'")
    dosage_form: str = Field(description="e.g. 'tablet', 'capsule', 'syrup'")
    dose: str = Field(description="e.g. '1 tablet', '5ml'")
    frequency: int = Field(ge=1, le=24, description="Times per frequency unit")
    frequency_unit: FrequencyUnit = FrequencyUnit.DAILY
    route: RouteOfAdministration = RouteOfAdministration.ORAL
    duration_days: int | None = Field(default=None, ge=1)
    quantity_dispensed: int | None = Field(default=None, ge=1)
    refills_allowed: int = Field(default=0, ge=0)
    special_instructions: str | None = None


class PrescriptionBase(BaseModel):
    patient_id: int
    doctor_id: int
    medical_record_id: int | None = None
    issued_date: date
    expiry_date: date | None = None
    medications: list[MedicationItem] = Field(min_length=1)
    notes: str | None = None
    requires_prior_authorization: bool = False

    @model_validator(mode="after")
    def validate_expiry(self) -> "PrescriptionBase":
        if self.expiry_date and self.expiry_date < self.issued_date:
            raise ValueError("Expiry date cannot be before issued date")
        return self

    model_config = ConfigDict(populate_by_name=True)


class PrescriptionCreate(PrescriptionBase):
    pass


class Prescription(PrescriptionBase):
    id: int
    prescription_number: str  # e.g. "RX-00789"
    status: PrescriptionStatus = PrescriptionStatus.DRAFT
    approved_by_id: int | None = None
    approved_at: datetime | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
