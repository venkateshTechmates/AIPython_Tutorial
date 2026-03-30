"""Part 7 — General-purpose utility tools."""

from datetime import date, datetime
from langchain_core.tools import tool
from pydantic import BaseModel, Field


class CalculateAgeInput(BaseModel):
    date_of_birth: str = Field(description="Date of birth in YYYY-MM-DD format")


class FormatDateInput(BaseModel):
    date_str: str = Field(description="Date string to format")
    output_format: str = Field(
        default="%B %d, %Y",
        description="Python strftime format string for the output",
    )


@tool("get_current_datetime")
async def get_current_datetime() -> dict:
    """Get the current date and time in multiple formats. Useful for scheduling and age calculations."""
    now = datetime.now()
    return {
        "datetime_iso": now.isoformat(),
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "human_readable": now.strftime("%A, %B %d, %Y at %I:%M %p"),
        "day_of_week": now.strftime("%A"),
        "unix_timestamp": int(now.timestamp()),
    }


@tool("calculate_patient_age", args_schema=CalculateAgeInput)
async def calculate_patient_age(date_of_birth: str) -> dict:
    """Calculate a patient's current age in years and months from their date of birth."""
    try:
        dob = date.fromisoformat(date_of_birth)
    except ValueError:
        return {"error": f"Invalid date format '{date_of_birth}'. Use YYYY-MM-DD."}

    today = date.today()
    if dob > today:
        return {"error": "Date of birth cannot be in the future."}

    age_years = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    age_months = (today.year - dob.year) * 12 + (today.month - dob.month)
    if today.day < dob.day:
        age_months -= 1

    age_category = (
        "Neonate (0–1 month)" if age_months < 1
        else "Infant (1–12 months)" if age_months < 12
        else "Child (1–12 years)" if age_years < 12
        else "Adolescent (12–18 years)" if age_years < 18
        else "Adult (18–65 years)" if age_years < 65
        else "Geriatric (65+)"
    )

    return {
        "date_of_birth": date_of_birth,
        "age_years": age_years,
        "age_months": age_months,
        "age_category": age_category,
        "next_birthday": f"{today.year + (1 if (today.month, today.day) >= (dob.month, dob.day) else 0)}-{dob.month:02d}-{dob.day:02d}",
    }


@tool("format_medical_date", args_schema=FormatDateInput)
async def format_medical_date(date_str: str, output_format: str = "%B %d, %Y") -> dict:
    """Parse and reformat a date string into a human-readable medical format."""
    formats_to_try = [
        "%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%Y/%m/%d",
        "%m-%d-%Y", "%d-%m-%Y", "%B %d, %Y", "%b %d, %Y",
    ]
    parsed_date = None
    for fmt in formats_to_try:
        try:
            parsed_date = datetime.strptime(date_str, fmt)
            break
        except ValueError:
            continue

    if parsed_date is None:
        return {"error": f"Could not parse date '{date_str}'. Try YYYY-MM-DD format."}

    return {
        "input": date_str,
        "formatted": parsed_date.strftime(output_format),
        "iso": parsed_date.strftime("%Y-%m-%d"),
        "day_of_week": parsed_date.strftime("%A"),
    }
