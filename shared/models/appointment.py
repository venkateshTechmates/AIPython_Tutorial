"""Appointment domain model with discriminated unions."""

from datetime import datetime
from enum import Enum
from typing import Annotated, Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class AppointmentStatus(str, Enum):
    SCHEDULED = "scheduled"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"


class AppointmentType(str, Enum):
    IN_PERSON = "in_person"
    TELEMEDICINE = "telemedicine"
    EMERGENCY = "emergency"
    FOLLOW_UP = "follow_up"


# Discriminated union: different appointment types carry different data
class InPersonAppointment(BaseModel):
    type: Literal["in_person"] = "in_person"
    room_number: str = Field(min_length=1, max_length=20)
    building: str | None = None


class TelemedicineAppointment(BaseModel):
    type: Literal["telemedicine"] = "telemedicine"
    meeting_link: str
    platform: str = "Zoom"


class EmergencyAppointment(BaseModel):
    type: Literal["emergency"] = "emergency"
    triage_level: int = Field(ge=1, le=5)  # 1=immediate, 5=non-urgent
    chief_complaint: str


AppointmentDetails = Annotated[
    InPersonAppointment | TelemedicineAppointment | EmergencyAppointment,
    Field(discriminator="type"),
]


class AppointmentBase(BaseModel):
    patient_id: int
    doctor_id: int
    scheduled_at: datetime
    duration_minutes: int = Field(default=30, ge=15, le=480)
    reason: str = Field(min_length=5, max_length=500)
    notes: str | None = None
    details: AppointmentDetails | None = None

    @field_validator("scheduled_at")
    @classmethod
    def validate_scheduled_time(cls, v: datetime) -> datetime:
        if v.hour < 6 or v.hour >= 22:
            raise ValueError("Appointments must be scheduled between 06:00 and 22:00")
        return v

    model_config = ConfigDict(populate_by_name=True)


class AppointmentCreate(AppointmentBase):
    pass


class Appointment(AppointmentBase):
    id: int
    appointment_number: str  # e.g. "APT-00123"
    status: AppointmentStatus = AppointmentStatus.SCHEDULED
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
