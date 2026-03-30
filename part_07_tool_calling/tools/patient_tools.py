"""Part 7 — DB-backed patient lookup tools."""

from langchain_core.tools import tool
from pydantic import BaseModel, Field


class GetPatientInput(BaseModel):
    patient_id: int = Field(description="The numeric patient ID to look up")


class SearchPatientInput(BaseModel):
    last_name: str = Field(description="Patient's last name for search")
    first_name: str | None = Field(default=None, description="Optional first name filter")


@tool("get_patient_by_id", args_schema=GetPatientInput)
async def get_patient_by_id(patient_id: int) -> dict:
    """Look up a patient record by their numeric patient ID."""
    # In a real system, this would query the database
    # Using mock data for demonstration
    mock_patients = {
        1: {"id": 1, "patient_number": "PAT-00001", "name": "Jane Doe", "dob": "1985-04-12",
            "blood_type": "O+", "allergies": ["penicillin"], "phone": "+1-555-0100"},
        2: {"id": 2, "patient_number": "PAT-00002", "name": "Robert Smith", "dob": "1972-08-22",
            "blood_type": "A+", "allergies": [], "phone": "+1-555-0101"},
        3: {"id": 3, "patient_number": "PAT-00003", "name": "Maria Garcia", "dob": "1990-01-05",
            "blood_type": "B-", "allergies": ["sulfa"], "phone": "+1-555-0102"},
    }
    patient = mock_patients.get(patient_id)
    if not patient:
        return {"error": f"Patient with ID {patient_id} not found"}
    return patient


@tool("search_patients_by_name", args_schema=SearchPatientInput)
async def search_patients_by_name(last_name: str, first_name: str | None = None) -> list[dict]:
    """Search for patients by last name (and optionally first name)."""
    mock_patients = [
        {"id": 1, "name": "Jane Doe", "patient_number": "PAT-00001"},
        {"id": 2, "name": "Robert Smith", "patient_number": "PAT-00002"},
        {"id": 3, "name": "Maria Garcia", "patient_number": "PAT-00003"},
    ]
    results = [p for p in mock_patients if last_name.lower() in p["name"].lower()]
    if first_name:
        results = [p for p in results if first_name.lower() in p["name"].lower()]
    return results if results else [{"message": "No patients found"}]
