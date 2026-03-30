"""Medical record domain model."""

import re
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator


class DiagnosisEntry(BaseModel):
    icd_code: str = Field(description="ICD-10 code, e.g. 'I21.0'")
    description: str
    is_primary: bool = False

    @field_validator("icd_code")
    @classmethod
    def validate_icd_code(cls, v: str) -> str:
        pattern = r"^[A-Z]\d{2}(\.\d{1,4})?$"
        if not re.match(pattern, v.upper()):
            raise ValueError(f"'{v}' is not a valid ICD-10 code (e.g. 'I21.0', 'J18')")
        return v.upper()


class VitalSigns(BaseModel):
    blood_pressure_systolic: int | None = Field(default=None, ge=60, le=250)
    blood_pressure_diastolic: int | None = Field(default=None, ge=40, le=150)
    heart_rate: int | None = Field(default=None, ge=30, le=300)
    temperature_celsius: float | None = Field(default=None, ge=34.0, le=43.0)
    respiratory_rate: int | None = Field(default=None, ge=8, le=60)
    oxygen_saturation: float | None = Field(default=None, ge=50.0, le=100.0)
    weight_kg: float | None = Field(default=None, ge=0.5, le=500.0)
    height_cm: float | None = Field(default=None, ge=30.0, le=280.0)


class MedicalRecordBase(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_id: int | None = None
    visit_date: datetime
    chief_complaint: str = Field(min_length=5, max_length=500)
    history_of_present_illness: str | None = None
    diagnoses: list[DiagnosisEntry] = Field(default_factory=list)
    vital_signs: VitalSigns | None = None
    treatment_plan: str | None = None
    follow_up_instructions: str | None = None
    is_confidential: bool = False

    model_config = ConfigDict(populate_by_name=True)


class MedicalRecordCreate(MedicalRecordBase):
    pass


class MedicalRecord(MedicalRecordBase):
    id: int
    record_number: str  # e.g. "REC-00456"
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
