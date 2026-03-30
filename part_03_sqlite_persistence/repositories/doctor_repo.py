"""Part 3 — Doctor repository (CRUD)."""

import json
from datetime import datetime
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from part_03_sqlite_persistence.database.models import DoctorORM
from shared.models.doctor import DoctorCreate


def _generate_doctor_number(doctor_id: int) -> str:
    return f"DOC-{doctor_id:05d}"


class DoctorRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, data: DoctorCreate) -> DoctorORM:
        doctor = DoctorORM(
            doctor_number="DOC-TEMP",
            first_name=data.first_name,
            last_name=data.last_name,
            specialty=data.specialty.value,
            email=data.email,
            phone=data.phone,
            license_number=data.license_number,
            department=data.department,
            years_of_experience=data.years_of_experience,
            consultation_fee=data.consultation_fee,
            available_days=json.dumps(data.available_days),
        )
        self.session.add(doctor)
        await self.session.flush()
        doctor.doctor_number = _generate_doctor_number(doctor.id)
        await self.session.flush()
        return doctor

    async def get_by_id(self, doctor_id: int) -> DoctorORM | None:
        result = await self.session.execute(
            select(DoctorORM).where(DoctorORM.id == doctor_id)
        )
        return result.scalar_one_or_none()

    async def get_by_specialty(self, specialty: str) -> list[DoctorORM]:
        result = await self.session.execute(
            select(DoctorORM)
            .where(DoctorORM.specialty == specialty, DoctorORM.is_active == True)
            .order_by(DoctorORM.last_name)
        )
        return list(result.scalars().all())

    async def get_all(self, offset: int = 0, limit: int = 100) -> list[DoctorORM]:
        result = await self.session.execute(
            select(DoctorORM)
            .where(DoctorORM.is_active == True)
            .offset(offset)
            .limit(limit)
            .order_by(DoctorORM.specialty, DoctorORM.last_name)
        )
        return list(result.scalars().all())

    async def count(self) -> int:
        result = await self.session.execute(
            select(func.count()).where(DoctorORM.is_active == True).select_from(DoctorORM)
        )
        return result.scalar_one()
