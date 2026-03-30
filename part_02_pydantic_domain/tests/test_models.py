"""Part 2 — Model test suite (runs without an API key)."""

import pytest
from datetime import date, datetime, timezone
from pydantic import ValidationError

from shared.models.patient import PatientCreate, Patient
from shared.models.doctor import DoctorCreate, Specialty
from shared.models.appointment import (
    AppointmentCreate,
    InPersonAppointment,
    TelemedicineAppointment,
    AppointmentStatus,
)
from shared.models.medical_record import MedicalRecordCreate, DiagnosisEntry, VitalSigns
from shared.models.prescription import PrescriptionCreate, MedicationItem, FrequencyUnit
from shared.models.billing import InvoiceCreate, BillingItem, BillingCategory


# ── Patient ───────────────────────────────────────────────────────────────────
class TestPatientModel:
    def test_valid_patient(self):
        p = PatientCreate(
            first_name="Jane",
            last_name="Doe",
            date_of_birth=date(1985, 4, 12),
            email="jane.doe@example.com",
            phone="+1-555-0100",
            address="123 Main St, Springfield, IL",
            blood_type="O+",
        )
        assert p.first_name == "Jane"
        assert p.blood_type == "O+"

    def test_future_dob_raises(self):
        with pytest.raises(ValidationError, match="future"):
            PatientCreate(
                first_name="Test",
                last_name="User",
                date_of_birth=date(2099, 1, 1),
                email="t@example.com",
                phone="+1-555-0000",
                address="123 Test St, City, ST 12345",
            )

    def test_invalid_blood_type_raises(self):
        with pytest.raises(ValidationError):
            PatientCreate(
                first_name="Test",
                last_name="User",
                date_of_birth=date(1990, 1, 1),
                email="t@example.com",
                phone="+1-555-0000",
                address="123 Test St, City, ST 12345",
                blood_type="XY",
            )

    def test_invalid_email_raises(self):
        with pytest.raises(ValidationError):
            PatientCreate(
                first_name="Test",
                last_name="User",
                date_of_birth=date(1990, 1, 1),
                email="not-an-email",
                phone="+1-555-0000",
                address="123 Test St, City, ST 12345",
            )

    def test_computed_fields(self):
        p = Patient(
            id=1,
            patient_number="PAT-00001",
            first_name="Jane",
            last_name="Doe",
            date_of_birth=date(1990, 6, 15),
            email="j@example.com",
            phone="+1-555-0000",
            address="123 Test St",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        assert p.full_name == "Jane Doe"
        assert isinstance(p.age, int)
        assert p.age > 0

    def test_json_serialization(self):
        p = PatientCreate(
            first_name="Alice",
            last_name="Smith",
            date_of_birth=date(1992, 3, 20),
            email="alice@example.com",
            phone="+1-555-0200",
            address="456 Oak Ave, Chicago, IL 60601",
        )
        json_str = p.model_dump_json()
        assert "Alice" in json_str
        assert "date_of_birth" in json_str


# ── Doctor ────────────────────────────────────────────────────────────────────
class TestDoctorModel:
    def test_valid_doctor(self):
        d = DoctorCreate(
            first_name="Sarah",
            last_name="Chen",
            specialty=Specialty.CARDIOLOGY,
            email="s.chen@hospital.com",
            phone="+1-555-0200",
            license_number="md-ca-98765",
            department="Cardiology",
            years_of_experience=15,
            consultation_fee=250.0,
        )
        assert d.license_number == "MD-CA-98765"  # uppercased

    def test_negative_experience_raises(self):
        with pytest.raises(ValidationError):
            DoctorCreate(
                first_name="X",
                last_name="Y",
                specialty=Specialty.GENERAL_PRACTICE,
                email="x@h.com",
                phone="+1-555-0000",
                license_number="ABC123",
                department="GP",
                years_of_experience=-1,
                consultation_fee=100.0,
            )

    def test_invalid_day_raises(self):
        with pytest.raises(ValidationError, match="valid day"):
            DoctorCreate(
                first_name="X",
                last_name="Y",
                specialty=Specialty.GENERAL_PRACTICE,
                email="x@h.com",
                phone="+1-555-0000",
                license_number="ABC123",
                department="GP",
                years_of_experience=5,
                consultation_fee=100.0,
                available_days=["Monday", "NotADay"],
            )


# ── Appointment ───────────────────────────────────────────────────────────────
class TestAppointmentModel:
    def test_in_person_appointment(self):
        a = AppointmentCreate(
            patient_id=1,
            doctor_id=1,
            scheduled_at=datetime(2026, 5, 15, 10, 30),
            reason="Annual checkup",
            details=InPersonAppointment(room_number="C-204"),
        )
        assert a.details.type == "in_person"
        assert a.details.room_number == "C-204"

    def test_telemedicine_appointment(self):
        a = AppointmentCreate(
            patient_id=1,
            doctor_id=2,
            scheduled_at=datetime(2026, 5, 20, 14, 0),
            reason="Follow-up",
            details=TelemedicineAppointment(meeting_link="https://zoom.us/j/123456"),
        )
        assert a.details.type == "telemedicine"

    def test_nighttime_appointment_raises(self):
        with pytest.raises(ValidationError, match="06:00"):
            AppointmentCreate(
                patient_id=1,
                doctor_id=1,
                scheduled_at=datetime(2026, 5, 15, 2, 0),  # 2 AM
                reason="Night visit",
            )


# ── Medical Record ────────────────────────────────────────────────────────────
class TestMedicalRecordModel:
    def test_valid_diagnosis_icd_code(self):
        d = DiagnosisEntry(icd_code="i21.0", description="Acute MI", is_primary=True)
        assert d.icd_code == "I21.0"  # normalized

    def test_invalid_icd_code_raises(self):
        with pytest.raises(ValidationError, match="ICD-10"):
            DiagnosisEntry(icd_code="INVALID", description="Test")

    def test_vital_signs_bounds(self):
        with pytest.raises(ValidationError):
            VitalSigns(heart_rate=500)  # above max


# ── Billing ───────────────────────────────────────────────────────────────────
class TestBillingModel:
    def test_invoice_total_computation(self):
        inv = InvoiceCreate(
            patient_id=1,
            issue_date=date(2026, 3, 1),
            due_date=date(2026, 3, 31),
            tax_percent=10.0,
            insurance_coverage_amount=50.0,
            items=[
                BillingItem(
                    description="Consultation",
                    category=BillingCategory.CONSULTATION,
                    quantity=1,
                    unit_price=100.0,
                )
            ],
        )
        assert inv.subtotal == 100.0
        assert inv.tax_amount == 10.0
        assert inv.total_amount == 110.0
        assert inv.patient_responsibility == 60.0

    def test_due_before_issue_raises(self):
        with pytest.raises(ValidationError, match="before issue"):
            InvoiceCreate(
                patient_id=1,
                issue_date=date(2026, 3, 31),
                due_date=date(2026, 3, 1),  # before issue date
                items=[
                    BillingItem(
                        description="Test",
                        category=BillingCategory.OTHER,
                        quantity=1,
                        unit_price=10.0,
                    )
                ],
            )

    def test_item_discount(self):
        item = BillingItem(
            description="ECG",
            category=BillingCategory.PROCEDURE,
            quantity=1,
            unit_price=200.0,
            discount_percent=25.0,
        )
        assert item.subtotal == 150.0
