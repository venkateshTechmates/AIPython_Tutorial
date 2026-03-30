"""Part 2 — Demonstration of all domain models with validation examples."""

import json
from datetime import date, datetime
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

# ── re-use shared models ──────────────────────────────────────────────────────
from shared.models.patient import PatientCreate, Patient
from shared.models.doctor import DoctorCreate, Specialty
from shared.models.appointment import AppointmentCreate, InPersonAppointment
from shared.models.medical_record import MedicalRecordCreate, DiagnosisEntry, VitalSigns
from shared.models.prescription import PrescriptionCreate, MedicationItem
from shared.models.billing import InvoiceCreate, BillingItem, BillingCategory

console = Console()


def demo_patient() -> None:
    console.rule("[bold cyan]Patient Model")

    patient_data = PatientCreate(
        first_name="Jane",
        last_name="Doe",
        date_of_birth=date(1985, 4, 12),
        email="jane.doe@email.com",
        phone="+1-555-0100",
        address="123 Main St, Springfield, IL 62701",
        blood_type="O+",
        allergies=["penicillin", "aspirin"],
        emergency_contact_name="John Doe",
        emergency_contact_phone="+1-555-0101",
        insurance_provider="BlueCross",
        insurance_policy_number="BC-987654",
    )
    console.print(Panel(patient_data.model_dump_json(indent=2), title="Valid Patient"))

    # Demonstrate validation error
    try:
        PatientCreate(
            first_name="Bob",
            last_name="Smith",
            date_of_birth=date(2030, 1, 1),  # future date — invalid!
            email="not-an-email",
            phone="123",
            address="Too short",
        )
    except Exception as e:
        console.print(f"[red]Expected ValidationError:[/red] {e}")


def demo_doctor() -> None:
    console.rule("[bold cyan]Doctor Model")

    doctor_data = DoctorCreate(
        first_name="Sarah",
        last_name="Chen",
        specialty=Specialty.CARDIOLOGY,
        email="s.chen@hospital.com",
        phone="+1-555-0200",
        license_number="md-ca-98765",  # will be uppercased by validator
        department="Cardiology",
        years_of_experience=15,
        consultation_fee=250.00,
    )
    console.print(Panel(doctor_data.model_dump_json(indent=2), title="Valid Doctor"))
    console.print(f"License (normalized): {doctor_data.license_number}")


def demo_appointment() -> None:
    console.rule("[bold cyan]Appointment Model (Discriminated Union)")

    appt = AppointmentCreate(
        patient_id=1,
        doctor_id=1,
        scheduled_at=datetime(2026, 5, 15, 10, 30),
        reason="Annual cardiology checkup",
        details=InPersonAppointment(room_number="C-204", building="Cardiology Wing"),
    )
    console.print(Panel(appt.model_dump_json(indent=2), title="In-Person Appointment"))


def demo_computed_fields() -> None:
    console.rule("[bold cyan]Computed Fields")
    from datetime import timezone

    full_patient = Patient(
        id=1,
        patient_number="PAT-00001",
        first_name="Jane",
        last_name="Doe",
        date_of_birth=date(1985, 4, 12),
        email="jane.doe@email.com",
        phone="+1-555-0100",
        address="123 Main St, Springfield, IL 62701",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    console.print(f"Full name: {full_patient.full_name}")
    console.print(f"Age: {full_patient.age}")


def demo_billing() -> None:
    console.rule("[bold cyan]Billing Model (Computed Totals)")

    invoice = InvoiceCreate(
        patient_id=1,
        issue_date=date.today(),
        due_date=date(2026, 4, 30),
        tax_percent=8.5,
        insurance_coverage_amount=200.00,
        items=[
            BillingItem(
                description="Cardiology Consultation",
                category=BillingCategory.CONSULTATION,
                quantity=1,
                unit_price=250.0,
            ),
            BillingItem(
                description="ECG Test",
                category=BillingCategory.PROCEDURE,
                quantity=1,
                unit_price=120.0,
                discount_percent=10.0,
            ),
        ],
    )
    console.print(f"Subtotal:             ${invoice.subtotal:.2f}")
    console.print(f"Tax ({invoice.tax_percent}%):        ${invoice.tax_amount:.2f}")
    console.print(f"Total:                ${invoice.total_amount:.2f}")
    console.print(f"Insurance covers:     ${invoice.insurance_coverage_amount:.2f}")
    console.print(f"Patient owes:         ${invoice.patient_responsibility:.2f}")


if __name__ == "__main__":
    demo_patient()
    demo_doctor()
    demo_appointment()
    demo_computed_fields()
    demo_billing()
