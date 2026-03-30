"""Part 2 — Custom reusable validators for hospital domain models."""

import re
from datetime import date


def validate_icd10_code(code: str) -> str:
    """Validate and normalize an ICD-10 code."""
    normalized = code.upper().strip()
    if not re.match(r"^[A-Z]\d{2}(\.\d{1,4})?$", normalized):
        raise ValueError(
            f"'{code}' is not a valid ICD-10 code. "
            "Expected format like 'I21.0', 'J18', or 'K92.1'"
        )
    return normalized


def validate_npi_number(npi: str) -> str:
    """Validate a National Provider Identifier (NPI) — 10 digits."""
    digits = re.sub(r"\D", "", npi)
    if len(digits) != 10:
        raise ValueError(f"NPI must be exactly 10 digits, got {len(digits)}")
    return digits


def validate_us_zip_code(zip_code: str) -> str:
    """Validate a US ZIP code (5-digit or ZIP+4)."""
    if not re.match(r"^\d{5}(-\d{4})?$", zip_code.strip()):
        raise ValueError(f"'{zip_code}' is not a valid US ZIP code")
    return zip_code.strip()


def must_be_past_date(v: date) -> date:
    """Ensure a date is in the past (useful for DOB, admission dates)."""
    if v > date.today():
        raise ValueError("Date must be in the past")
    return v


def must_be_future_date(v: date) -> date:
    """Ensure a date is in the future (useful for appointment dates)."""
    if v < date.today():
        raise ValueError("Date must be in the future")
    return v
