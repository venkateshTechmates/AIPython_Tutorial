import type { PartData } from "../../types";

export const part02: PartData = {
  id: "02",
  title: "Pydantic Domain Models",
  goal: "Model the entire hospital domain with Pydantic v2 validators, computed fields, and discriminated unions.",
  phase: 1,
  phaseLabel: "Core Foundations",
  folder: "part_02_pydantic",
  estimatedHours: 3,
  difficulty: "beginner",
  prerequisites: ["01"],
  unlocks: ["03"],
  whatYouBuild: [
    { label: "POST /patients/validate", description: "Validate a patient record" },
    { label: "POST /appointments/validate", description: "Validate appointment data" },
    { label: "POST /billing/validate", description: "Validate billing records" },
    { label: "GET /schema/{model}", description: "Retrieve JSON schema for any model" },
  ],
  mermaidDiagram: `
classDiagram
  class Patient {
    +str id
    +str name
    +date date_of_birth
    +BloodType blood_type
    +int age
    +validate_dob()
  }
  class Doctor {
    +str id
    +str name
    +Specialty specialty
    +float consultation_fee
  }
  class Appointment {
    +str id
    +str patient_id
    +str doctor_id
    +datetime scheduled_at
    +AppointmentStatus status
    +validate_future_date()
  }
  class Invoice {
    +str id
    +float amount
    +bool insurance_covered
    +float patient_responsibility
  }
  Patient "1" --> "*" Appointment
  Doctor "1" --> "*" Appointment
  Appointment "1" --> "0..1" Invoice
  `,
  concepts: [
    {
      id: "field-validators",
      title: "Pydantic v2 Field Validators",
      explanation:
        "Pydantic v2 uses @field_validator to validate individual fields. Validators run after the field type is confirmed, giving you access to the coerced value.",
      code: {
        language: "python",
        filename: "shared/models/patient.py",
        snippet: `from pydantic import BaseModel, field_validator
from datetime import date

class Patient(BaseModel):
    name: str
    date_of_birth: date

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Patient name cannot be blank")
        return v.title()  # Normalise to title case

    @field_validator("date_of_birth")
    @classmethod
    def dob_in_past(cls, v: date) -> date:
        if v >= date.today():
            raise ValueError("Date of birth must be in the past")
        return v`,
      },
      glossaryTerms: ["Pydantic", "Validator"],
    },
    {
      id: "computed-fields",
      title: "Computed Fields",
      explanation:
        "@computed_field lets you derive values from other fields. The computed field is included in serialization but not required in the input.",
      code: {
        language: "python",
        filename: "shared/models/patient.py",
        snippet: `from pydantic import computed_field
from datetime import date

class Patient(BaseModel):
    date_of_birth: date

    @computed_field
    @property
    def age(self) -> int:
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) <
            (self.date_of_birth.month, self.date_of_birth.day)
        )

    @computed_field
    @property
    def age_category(self) -> str:
        if self.age < 18: return "pediatric"
        if self.age < 65: return "adult"
        return "senior"`,
      },
    },
    {
      id: "discriminated-unions",
      title: "Discriminated Unions",
      explanation:
        "Discriminated unions select the correct model based on a literal 'type' field. This is perfect for polymorphic events like AppointmentEvent.",
      code: {
        language: "python",
        filename: "shared/models/events.py",
        snippet: `from typing import Literal, Annotated, Union
from pydantic import BaseModel, Field

class ScheduledEvent(BaseModel):
    type: Literal["scheduled"]
    appointment_id: str
    scheduled_at: datetime

class CancelledEvent(BaseModel):
    type: Literal["cancelled"]
    appointment_id: str
    reason: str

AppointmentEvent = Annotated[
    Union[ScheduledEvent, CancelledEvent],
    Field(discriminator="type")
]`,
      },
      glossaryTerms: ["Discriminated Union", "Pydantic"],
    },
  ],
  steps: [
    {
      number: 1,
      title: "Create the Patient model",
      description:
        "Define Patient with field validators for DOB, blood type enum, and a computed age field.",
    },
    {
      number: 2,
      title: "Create Doctor and Specialty models",
      description:
        "Define Doctor with specialties as StrEnum and consultation fees with range validation.",
    },
    {
      number: 3,
      title: "Create Appointment model",
      description:
        "Use @model_validator to ensure appointments can't be booked in the past.",
    },
    {
      number: 4,
      title: "Create Invoice with insurance logic",
      description:
        "Add a computed patient_responsibility field that applies 20% co-pay when insurance is active.",
    },
    {
      number: 5,
      title: "Wire FastAPI validation endpoints",
      description: "Return model.model_json_schema() from GET /schema/{model}.",
    },
  ],
  acceptanceCriteria: [
    { id: "ac1", text: "Patient model rejects future dates of birth" },
    { id: "ac2", text: "Patient.age computed field returns correct integer age" },
    { id: "ac3", text: "Appointment rejects past scheduled_at dates" },
    { id: "ac4", text: "Invoice.patient_responsibility applies 80/20 insurance split" },
    { id: "ac5", text: "GET /schema/patient returns valid JSON Schema" },
  ],
  gotchas: [
    {
      error: "TypeError: field_validator missing @classmethod",
      cause: "Pydantic v2 requires @classmethod decorator on field validators",
      fix: "Add @classmethod above @field_validator on every validator method",
    },
    {
      error: "computed_field not serialised in model.dict()",
      cause: "model.dict() is Pydantic v1 API",
      fix: "Use model.model_dump() in Pydantic v2",
    },
  ],
  resources: [
    { title: "Pydantic v2 Docs", url: "https://docs.pydantic.dev/latest/" },
    { title: "Field Validators", url: "https://docs.pydantic.dev/latest/concepts/validators/" },
  ],
};
