"""Part 7 — tools package exports."""

from .patient_tools import get_patient_by_id, search_patients_by_name
from .appointment_tools import schedule_appointment, check_doctor_availability
from .billing_tools import get_invoice_by_id, calculate_bill, apply_discount
from .medical_tools import search_drug_interactions, lookup_icd10_code, get_drug_information
from .utility_tools import get_current_datetime, calculate_patient_age, format_medical_date

ALL_TOOLS = [
    get_patient_by_id,
    search_patients_by_name,
    schedule_appointment,
    check_doctor_availability,
    get_invoice_by_id,
    calculate_bill,
    apply_discount,
    search_drug_interactions,
    lookup_icd10_code,
    get_drug_information,
    get_current_datetime,
    calculate_patient_age,
    format_medical_date,
]

__all__ = [
    "get_patient_by_id",
    "search_patients_by_name",
    "schedule_appointment",
    "check_doctor_availability",
    "get_invoice_by_id",
    "calculate_bill",
    "apply_discount",
    "search_drug_interactions",
    "lookup_icd10_code",
    "get_drug_information",
    "get_current_datetime",
    "calculate_patient_age",
    "format_medical_date",
    "ALL_TOOLS",
]
