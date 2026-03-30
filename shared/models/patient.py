"""Patient domain model."""

from datetime import date, datetime
from typing import Annotated
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, computed_field


class PatientBase(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    date_of_birth: date
    email: EmailStr
    phone: str = Field(pattern=r"^\+?[\d\s\-\(\)]{7,20}$")
    address: str = Field(min_length=5, max_length=500)
    blood_type: str | None = Field(default=None, pattern=r"^(A|B|AB|O)[+-]$")
    allergies: list[str] = Field(default_factory=list)
    emergency_contact_name: str | None = None
    emergency_contact_phone: str | None = None
    insurance_provider: str | None = None
    insurance_policy_number: str | None = None

    @field_validator("date_of_birth")
    @classmethod
    def validate_dob(cls, v: date) -> date:
        today = date.today()
        if v > today:
            raise ValueError("Date of birth cannot be in the future")
        age = (today - v).days // 365
        if age > 150:
            raise ValueError("Date of birth results in unrealistic age")
        return v

    @field_validator("phone")
    @classmethod
    def normalize_phone(cls, v: str) -> str:
        return v.strip()

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "examples": [
                {
                    "first_name": "Jane",
                    "last_name": "Doe",
                    "date_of_birth": "1985-04-12",
                    "email": "jane.doe@example.com",
                    "phone": "+1-555-0100",
                    "address": "123 Main St, Springfield, IL 62701",
                    "blood_type": "O+",
                    "allergies": ["penicillin"],
                }
            ]
        },
    )


class PatientCreate(PatientBase):
    pass


class PatientUpdate(BaseModel):
    first_name: str | None = Field(default=None, min_length=1, max_length=100)
    last_name: str | None = Field(default=None, min_length=1, max_length=100)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, pattern=r"^\+?[\d\s\-\(\)]{7,20}$")
    address: str | None = Field(default=None, min_length=5, max_length=500)
    blood_type: str | None = Field(default=None, pattern=r"^(A|B|AB|O)[+-]$")
    allergies: list[str] | None = None
    emergency_contact_name: str | None = None
    emergency_contact_phone: str | None = None
    insurance_provider: str | None = None
    insurance_policy_number: str | None = None

    model_config = ConfigDict(populate_by_name=True)


class Patient(PatientBase):
    id: int
    patient_number: str  # e.g. "PAT-00042"
    created_at: datetime
    updated_at: datetime
    is_active: bool = True

    @computed_field
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @computed_field
    @property
    def age(self) -> int:
        today = date.today()
        dob = self.date_of_birth
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
