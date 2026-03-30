"""Part 3 — Repository tests using in-memory SQLite."""

import pytest
import pytest_asyncio
from datetime import date, datetime
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool

from shared.database.base import Base
from part_03_sqlite_persistence.database.models import PatientORM, DoctorORM, AppointmentORM
from part_03_sqlite_persistence.repositories.patient_repo import PatientRepository
from part_03_sqlite_persistence.repositories.doctor_repo import DoctorRepository
from part_03_sqlite_persistence.repositories.appointment_repo import AppointmentRepository
from shared.models.patient import PatientCreate, PatientUpdate
from shared.models.doctor import DoctorCreate, Specialty
from shared.models.appointment import AppointmentCreate, AppointmentStatus, InPersonAppointment


# ── Test fixtures ─────────────────────────────────────────────────────────────

@pytest.fixture(scope="function")
async def test_engine():
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture(scope="function")
async def session(test_engine):
    session_factory = async_sessionmaker(bind=test_engine, expire_on_commit=False)
    async with session_factory() as s:
        yield s


@pytest.fixture
def patient_repo(session):
    return PatientRepository(session)


@pytest.fixture
def doctor_repo(session):
    return DoctorRepository(session)


@pytest.fixture
def appointment_repo(session):
    return AppointmentRepository(session)


def make_patient(idx: int = 1) -> PatientCreate:
    return PatientCreate(
        first_name=f"Test{idx}",
        last_name="Patient",
        date_of_birth=date(1990, 1, 1),
        email=f"test{idx}@example.com",
        phone="+1-555-0000",
        address=f"{idx} Test Street, City, ST 12345",
    )


def make_doctor(idx: int = 1) -> DoctorCreate:
    return DoctorCreate(
        first_name=f"Dr{idx}",
        last_name="Smith",
        specialty=Specialty.GENERAL_PRACTICE,
        email=f"doctor{idx}@hospital.com",
        phone="+1-555-0001",
        license_number=f"MD-TEST-{idx:05d}",
        department="Primary Care",
        years_of_experience=10,
        consultation_fee=150.0,
    )


# ── Patient tests ─────────────────────────────────────────────────────────────

class TestPatientRepository:
    async def test_create_patient(self, patient_repo, session):
        patient = await patient_repo.create(make_patient(1))
        await session.commit()
        assert patient.id is not None
        assert patient.patient_number.startswith("PAT-")
        assert patient.email == "test1@example.com"

    async def test_get_by_id(self, patient_repo, session):
        created = await patient_repo.create(make_patient(2))
        await session.commit()
        fetched = await patient_repo.get_by_id(created.id)
        assert fetched is not None
        assert fetched.first_name == "Test2"

    async def test_get_by_email(self, patient_repo, session):
        await patient_repo.create(make_patient(3))
        await session.commit()
        fetched = await patient_repo.get_by_email("test3@example.com")
        assert fetched is not None

    async def test_get_nonexistent_returns_none(self, patient_repo):
        result = await patient_repo.get_by_id(99999)
        assert result is None

    async def test_update_patient(self, patient_repo, session):
        patient = await patient_repo.create(make_patient(4))
        await session.commit()
        updated = await patient_repo.update(patient.id, PatientUpdate(first_name="Updated"))
        await session.commit()
        assert updated.first_name == "Updated"

    async def test_soft_delete(self, patient_repo, session):
        patient = await patient_repo.create(make_patient(5))
        await session.commit()
        result = await patient_repo.delete(patient.id)
        await session.commit()
        assert result is True
        fetched = await patient_repo.get_by_id(patient.id)
        assert fetched.is_active is False

    async def test_count(self, patient_repo, session):
        for i in range(10, 13):
            await patient_repo.create(make_patient(i))
        await session.commit()
        count = await patient_repo.count()
        assert count >= 3


# ── Doctor tests ──────────────────────────────────────────────────────────────

class TestDoctorRepository:
    async def test_create_doctor(self, doctor_repo, session):
        doctor = await doctor_repo.create(make_doctor(1))
        await session.commit()
        assert doctor.id is not None
        assert doctor.doctor_number.startswith("DOC-")

    async def test_get_by_specialty(self, doctor_repo, session):
        await doctor_repo.create(make_doctor(2))
        await session.commit()
        doctors = await doctor_repo.get_by_specialty("general_practice")
        assert len(doctors) >= 1


# ── Appointment tests ─────────────────────────────────────────────────────────

class TestAppointmentRepository:
    async def test_create_appointment(self, patient_repo, doctor_repo, appointment_repo, session):
        patient = await patient_repo.create(make_patient(20))
        doctor = await doctor_repo.create(make_doctor(20))
        await session.commit()

        appt = await appointment_repo.create(
            AppointmentCreate(
                patient_id=patient.id,
                doctor_id=doctor.id,
                scheduled_at=datetime(2026, 6, 1, 10, 0),
                reason="Routine checkup",
                details=InPersonAppointment(room_number="A-101"),
            )
        )
        await session.commit()
        assert appt.appointment_number.startswith("APT-")
        assert appt.status == "scheduled"

    async def test_update_status(self, patient_repo, doctor_repo, appointment_repo, session):
        patient = await patient_repo.create(make_patient(21))
        doctor = await doctor_repo.create(make_doctor(21))
        await session.commit()
        appt = await appointment_repo.create(
            AppointmentCreate(
                patient_id=patient.id,
                doctor_id=doctor.id,
                scheduled_at=datetime(2026, 6, 2, 12, 0),
                reason="Follow-up",
            )
        )
        await session.commit()
        updated = await appointment_repo.update_status(appt.id, AppointmentStatus.CONFIRMED)
        await session.commit()
        assert updated.status == "confirmed"
