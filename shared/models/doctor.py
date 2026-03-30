"""Doctor domain model."""

from datetime import datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, computed_field


class Specialty(str, Enum):
    CARDIOLOGY = "cardiology"
    NEUROLOGY = "neurology"
    GENERAL_PRACTICE = "general_practice"
    ORTHOPEDICS = "orthopedics"
    PEDIATRICS = "pediatrics"
    ONCOLOGY = "oncology"
    PSYCHIATRY = "psychiatry"
    RADIOLOGY = "radiology"
    EMERGENCY = "emergency"
    SURGERY = "surgery"
    INTERNAL_MEDICINE = "internal_medicine"
    DERMATOLOGY = "dermatology"


class DoctorBase(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    specialty: Specialty
    email: EmailStr
    phone: str = Field(pattern=r"^\+?[\d\s\-\(\)]{7,20}$")
    license_number: str = Field(min_length=5, max_length=50)
    department: str = Field(min_length=1, max_length=100)
    years_of_experience: int = Field(ge=0, le=60)
    consultation_fee: float = Field(gt=0)
    available_days: list[str] = Field(
        default_factory=lambda: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    )

    @field_validator("license_number")
    @classmethod
    def validate_license(cls, v: str) -> str:
        return v.upper().strip()

    @field_validator("available_days")
    @classmethod
    def validate_days(cls, v: list[str]) -> list[str]:
        valid_days = {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"}
        for day in v:
            if day not in valid_days:
                raise ValueError(f"'{day}' is not a valid day of the week")
        return v

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "examples": [
                {
                    "first_name": "Dr. Sarah",
                    "last_name": "Chen",
                    "specialty": "cardiology",
                    "email": "s.chen@hospital.com",
                    "phone": "+1-555-0200",
                    "license_number": "MD-CA-98765",
                    "department": "Cardiology",
                    "years_of_experience": 15,
                    "consultation_fee": 250.00,
                }
            ]
        },
    )


class DoctorCreate(DoctorBase):
    pass


class Doctor(DoctorBase):
    id: int
    doctor_number: str  # e.g. "DOC-00007"
    created_at: datetime
    updated_at: datetime
    is_active: bool = True

    @computed_field
    @property
    def full_name(self) -> str:
        return f"Dr. {self.first_name} {self.last_name}"

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
