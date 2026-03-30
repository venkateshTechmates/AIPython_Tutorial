"""Shared domain models package."""

from shared.models.patient import Patient, PatientCreate, PatientUpdate
from shared.models.doctor import Doctor, DoctorCreate, Specialty
from shared.models.appointment import Appointment, AppointmentCreate, AppointmentStatus
from shared.models.medical_record import MedicalRecord, MedicalRecordCreate
from shared.models.prescription import Prescription, PrescriptionCreate
from shared.models.billing import Invoice, BillingItem, BillingStatus

__all__ = [
    "Patient", "PatientCreate", "PatientUpdate",
    "Doctor", "DoctorCreate", "Specialty",
    "Appointment", "AppointmentCreate", "AppointmentStatus",
    "MedicalRecord", "MedicalRecordCreate",
    "Prescription", "PrescriptionCreate",
    "Invoice", "BillingItem", "BillingStatus",
]
