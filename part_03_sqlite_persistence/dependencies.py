"""Part 3 — FastAPI DB session dependency."""

from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from part_03_sqlite_persistence.database.base import AsyncSessionLocal

from part_03_sqlite_persistence.repositories.patient_repo import PatientRepository
from part_03_sqlite_persistence.repositories.doctor_repo import DoctorRepository
from part_03_sqlite_persistence.repositories.appointment_repo import AppointmentRepository


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def get_patient_repo(session: AsyncSession = Depends(get_db)) -> PatientRepository:
    return PatientRepository(session)


async def get_doctor_repo(session: AsyncSession = Depends(get_db)) -> DoctorRepository:
    return DoctorRepository(session)


async def get_appointment_repo(session: AsyncSession = Depends(get_db)) -> AppointmentRepository:
    return AppointmentRepository(session)
