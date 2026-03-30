"""Part 3 — Seed script: populate DB with realistic hospital data."""

import asyncio
import json
from datetime import date, datetime, timedelta
import random

from part_03_sqlite_persistence.database.base import init_tables, engine
from part_03_sqlite_persistence.database.models import PatientORM, DoctorORM, AppointmentORM
from part_03_sqlite_persistence.repositories.patient_repo import PatientRepository
from part_03_sqlite_persistence.repositories.doctor_repo import DoctorRepository
from part_03_sqlite_persistence.repositories.appointment_repo import AppointmentRepository
from part_03_sqlite_persistence.database.base import AsyncSessionLocal
from shared.models.patient import PatientCreate
from shared.models.doctor import DoctorCreate, Specialty
from shared.models.appointment import AppointmentCreate, InPersonAppointment


SAMPLE_PATIENTS = [
    {"first_name": "Jane", "last_name": "Doe", "dob": date(1985, 4, 12), "email": "jane.doe@email.com", "blood_type": "O+", "allergies": ["penicillin"]},
    {"first_name": "Robert", "last_name": "Smith", "dob": date(1972, 8, 22), "email": "r.smith@email.com", "blood_type": "A+", "allergies": []},
    {"first_name": "Maria", "last_name": "Garcia", "dob": date(1990, 1, 5), "email": "maria.g@email.com", "blood_type": "B-", "allergies": ["sulfa", "ibuprofen"]},
    {"first_name": "James", "last_name": "Wilson", "dob": date(1965, 11, 30), "email": "j.wilson@email.com", "blood_type": "AB+", "allergies": []},
    {"first_name": "Emily", "last_name": "Johnson", "dob": date(2001, 6, 18), "email": "e.johnson@email.com", "blood_type": "O-", "allergies": ["latex"]},
    {"first_name": "Michael", "last_name": "Brown", "dob": date(1958, 3, 7), "email": "m.brown@email.com", "blood_type": "A-", "allergies": []},
    {"first_name": "Sarah", "last_name": "Davis", "dob": date(1995, 9, 14), "email": "s.davis@email.com", "blood_type": "B+", "allergies": ["aspirin"]},
    {"first_name": "David", "last_name": "Martinez", "dob": date(1980, 12, 3), "email": "d.martinez@email.com", "blood_type": "O+", "allergies": []},
    {"first_name": "Lisa", "last_name": "Anderson", "dob": date(1968, 7, 25), "email": "l.anderson@email.com", "blood_type": "A+", "allergies": ["codeine"]},
    {"first_name": "Christopher", "last_name": "Taylor", "dob": date(1975, 2, 19), "email": "c.taylor@email.com", "blood_type": "AB-", "allergies": []},
    {"first_name": "Amanda", "last_name": "Thomas", "dob": date(1988, 5, 30), "email": "a.thomas@email.com", "blood_type": "O+", "allergies": []},
    {"first_name": "Matthew", "last_name": "Hernandez", "dob": date(1992, 10, 11), "email": "m.hernandez@email.com", "blood_type": "B+", "allergies": ["shellfish"]},
    {"first_name": "Jennifer", "last_name": "Young", "dob": date(1970, 4, 6), "email": "j.young@email.com", "blood_type": "A+", "allergies": []},
    {"first_name": "Andrew", "last_name": "Lee", "dob": date(1983, 8, 17), "email": "a.lee@email.com", "blood_type": "O-", "allergies": ["peanuts"]},
    {"first_name": "Jessica", "last_name": "White", "dob": date(1997, 1, 28), "email": "j.white@email.com", "blood_type": "B-", "allergies": []},
    {"first_name": "Joshua", "last_name": "Harris", "dob": date(1962, 6, 9), "email": "j.harris@email.com", "blood_type": "A-", "allergies": []},
    {"first_name": "Ashley", "last_name": "Clark", "dob": date(2003, 3, 21), "email": "a.clark@email.com", "blood_type": "AB+", "allergies": ["gluten"]},
    {"first_name": "Daniel", "last_name": "Lewis", "dob": date(1978, 11, 14), "email": "d.lewis@email.com", "blood_type": "O+", "allergies": []},
    {"first_name": "Megan", "last_name": "Robinson", "dob": date(1986, 7, 2), "email": "m.robinson@email.com", "blood_type": "A+", "allergies": ["penicillin"]},
    {"first_name": "Ryan", "last_name": "Walker", "dob": date(1999, 12, 25), "email": "r.walker@email.com", "blood_type": "B+", "allergies": []},
    {"first_name": "Hannah", "last_name": "Hall", "dob": date(1991, 9, 8), "email": "h.hall@email.com", "blood_type": "O+", "allergies": []},
    {"first_name": "Kevin", "last_name": "Allen", "dob": date(1955, 5, 16), "email": "k.allen@email.com", "blood_type": "A+", "allergies": ["aspirin", "ibuprofen"]},
]

SAMPLE_DOCTORS = [
    {"first_name": "Katherine", "last_name": "Chen", "specialty": Specialty.CARDIOLOGY, "license": "MD-CA-10001", "department": "Cardiology", "exp": 18, "fee": 300.0},
    {"first_name": "Marcus", "last_name": "Williams", "specialty": Specialty.NEUROLOGY, "license": "MD-NY-10002", "department": "Neurology", "exp": 12, "fee": 350.0},
    {"first_name": "Priya", "last_name": "Patel", "specialty": Specialty.GENERAL_PRACTICE, "license": "MD-TX-10003", "department": "Primary Care", "exp": 8, "fee": 150.0},
    {"first_name": "James", "last_name": "Murphy", "specialty": Specialty.ORTHOPEDICS, "license": "MD-FL-10004", "department": "Orthopedics", "exp": 20, "fee": 280.0},
    {"first_name": "Elena", "last_name": "Rodriguez", "specialty": Specialty.PEDIATRICS, "license": "MD-WA-10005", "department": "Pediatrics", "exp": 10, "fee": 200.0},
    {"first_name": "David", "last_name": "Kim", "specialty": Specialty.EMERGENCY, "license": "MD-IL-10006", "department": "Emergency", "exp": 7, "fee": 400.0},
    {"first_name": "Amara", "last_name": "Okonkwo", "specialty": Specialty.ONCOLOGY, "license": "MD-OH-10007", "department": "Oncology", "exp": 15, "fee": 500.0},
    {"first_name": "Thomas", "last_name": "Fischer", "specialty": Specialty.PSYCHIATRY, "license": "MD-MA-10008", "department": "Behavioral Health", "exp": 11, "fee": 320.0},
    {"first_name": "Nina", "last_name": "Johansson", "specialty": Specialty.RADIOLOGY, "license": "MD-CO-10009", "department": "Radiology", "exp": 9, "fee": 250.0},
    {"first_name": "Carlos", "last_name": "Santos", "specialty": Specialty.INTERNAL_MEDICINE, "license": "MD-GA-10010", "department": "Internal Medicine", "exp": 14, "fee": 230.0},
]

REASONS = [
    "Annual physical examination",
    "Follow-up for hypertension management",
    "Chest pain evaluation",
    "Headache and dizziness workup",
    "Knee pain assessment",
    "Vaccination consultation",
    "Diabetes management review",
    "Skin rash evaluation",
    "Pre-operative assessment",
    "Medication review and adjustment",
    "Back pain consultation",
    "Mental health assessment",
    "Respiratory infection follow-up",
    "Sleep disorder evaluation",
    "Thyroid function check",
]


async def seed_database() -> None:
    await init_tables()

    async with AsyncSessionLocal() as session:
        patient_repo = PatientRepository(session)
        doctor_repo = DoctorRepository(session)
        appointment_repo = AppointmentRepository(session)

        # Seed patients
        patient_ids = []
        for idx, p in enumerate(SAMPLE_PATIENTS):
            existing = await patient_repo.get_by_email(p["email"])
            if existing:
                patient_ids.append(existing.id)
                continue
            patient = await patient_repo.create(
                PatientCreate(
                    first_name=p["first_name"],
                    last_name=p["last_name"],
                    date_of_birth=p["dob"],
                    email=p["email"],
                    phone=f"+1-555-{1000 + idx:04d}",
                    address=f"{100 + idx} Hospital Way, Medical City, MC {10000 + idx}",
                    blood_type=p["blood_type"],
                    allergies=p["allergies"],
                )
            )
            patient_ids.append(patient.id)
        print(f"Seeded {len(patient_ids)} patients")

        # Seed doctors
        doctor_ids = []
        for d in SAMPLE_DOCTORS:
            doctor = await doctor_repo.create(
                DoctorCreate(
                    first_name=d["first_name"],
                    last_name=d["last_name"],
                    specialty=d["specialty"],
                    email=f"{d['first_name'].lower()}.{d['last_name'].lower()}@hospital.com",
                    phone=f"+1-555-{random.randint(2000, 9999)}",
                    license_number=d["license"],
                    department=d["department"],
                    years_of_experience=d["exp"],
                    consultation_fee=d["fee"],
                )
            )
            doctor_ids.append(doctor.id)
        print(f"Seeded {len(doctor_ids)} doctors")

        # Seed appointments (50)
        base_date = datetime(2026, 4, 1, 9, 0)
        for i in range(50):
            patient_id = random.choice(patient_ids)
            doctor_id = random.choice(doctor_ids)
            delta_days = random.randint(0, 60)
            delta_hours = random.choice([0, 1, 2, 3, 4, 5, 6, 7])
            scheduled_at = base_date + timedelta(days=delta_days, hours=delta_hours)

            await appointment_repo.create(
                AppointmentCreate(
                    patient_id=patient_id,
                    doctor_id=doctor_id,
                    scheduled_at=scheduled_at,
                    duration_minutes=random.choice([15, 30, 45, 60]),
                    reason=random.choice(REASONS),
                    details=InPersonAppointment(
                        room_number=f"{random.choice('ABCDE')}-{random.randint(100, 550)}"
                    ),
                )
            )
        print("Seeded 50 appointments")
        await session.commit()

    print("Database seeding complete!")


if __name__ == "__main__":
    asyncio.run(seed_database())
