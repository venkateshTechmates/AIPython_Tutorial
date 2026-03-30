"""Part 7 — Appointment scheduling tools."""

from datetime import datetime, timedelta
from langchain_core.tools import tool
from pydantic import BaseModel, Field


class ScheduleAppointmentInput(BaseModel):
    patient_id: int = Field(description="Patient ID to schedule for")
    doctor_specialty: str = Field(description="Medical specialty needed (e.g., 'cardiology')")
    preferred_date: str = Field(description="Preferred date in YYYY-MM-DD format")
    reason: str = Field(description="Reason for the appointment (brief description)")


class CheckAvailabilityInput(BaseModel):
    doctor_id: int = Field(description="Doctor ID to check availability for")
    date: str = Field(description="Date to check in YYYY-MM-DD format")


@tool("schedule_appointment", args_schema=ScheduleAppointmentInput)
async def schedule_appointment(
    patient_id: int,
    doctor_specialty: str,
    preferred_date: str,
    reason: str,
) -> dict:
    """Schedule a new appointment for a patient with a doctor of the specified specialty."""
    # Mock implementation — real version would query the DB
    specialty_doctors = {
        "cardiology": {"id": 1, "name": "Dr. Katherine Chen", "fee": 300.0},
        "neurology": {"id": 2, "name": "Dr. Marcus Williams", "fee": 350.0},
        "general_practice": {"id": 3, "name": "Dr. Priya Patel", "fee": 150.0},
        "orthopedics": {"id": 4, "name": "Dr. James Murphy", "fee": 280.0},
    }

    doctor = specialty_doctors.get(doctor_specialty.lower())
    if not doctor:
        return {
            "error": f"No doctor found for specialty '{doctor_specialty}'. "
                     f"Available: {', '.join(specialty_doctors.keys())}"
        }

    appointment_number = f"APT-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    return {
        "appointment_number": appointment_number,
        "patient_id": patient_id,
        "doctor": doctor["name"],
        "specialty": doctor_specialty,
        "scheduled_at": f"{preferred_date} 10:00 AM",
        "duration_minutes": 30,
        "reason": reason,
        "consultation_fee": doctor["fee"],
        "status": "scheduled",
        "confirmation": f"Appointment {appointment_number} scheduled successfully!",
    }


@tool("check_doctor_availability", args_schema=CheckAvailabilityInput)
async def check_doctor_availability(doctor_id: int, date: str) -> dict:
    """Check available appointment slots for a specific doctor on a given date."""
    # Mock available slots
    available_slots = [
        "09:00 AM", "09:30 AM", "10:30 AM", "11:00 AM",
        "02:00 PM", "02:30 PM", "03:00 PM", "04:00 PM",
    ]
    return {
        "doctor_id": doctor_id,
        "date": date,
        "available_slots": available_slots,
        "total_slots": len(available_slots),
    }
