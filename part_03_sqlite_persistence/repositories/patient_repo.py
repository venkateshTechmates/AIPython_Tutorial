"""Part 3 — Patient repository (CRUD)."""

import json
from datetime import datetime
from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession

from part_03_sqlite_persistence.database.models import PatientORM
from shared.models.patient import PatientCreate, PatientUpdate


def _generate_patient_number(patient_id: int) -> str:
    return f"PAT-{patient_id:05d}"


class PatientRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, data: PatientCreate) -> PatientORM:
        patient = PatientORM(
            patient_number="PAT-TEMP",  # updated after flush
            first_name=data.first_name,
            last_name=data.last_name,
            date_of_birth=data.date_of_birth,
            email=data.email,
            phone=data.phone,
            address=data.address,
            blood_type=data.blood_type,
            allergies=json.dumps(data.allergies) if data.allergies else None,
            emergency_contact_name=data.emergency_contact_name,
            emergency_contact_phone=data.emergency_contact_phone,
            insurance_provider=data.insurance_provider,
            insurance_policy_number=data.insurance_policy_number,
        )
        self.session.add(patient)
        await self.session.flush()  # get the assigned id
        patient.patient_number = _generate_patient_number(patient.id)
        await self.session.flush()
        return patient

    async def get_by_id(self, patient_id: int) -> PatientORM | None:
        result = await self.session.execute(
            select(PatientORM).where(PatientORM.id == patient_id)
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> PatientORM | None:
        result = await self.session.execute(
            select(PatientORM).where(PatientORM.email == email)
        )
        return result.scalar_one_or_none()

    async def get_all(self, offset: int = 0, limit: int = 100) -> list[PatientORM]:
        result = await self.session.execute(
            select(PatientORM)
            .where(PatientORM.is_active == True)
            .offset(offset)
            .limit(limit)
            .order_by(PatientORM.last_name, PatientORM.first_name)
        )
        return list(result.scalars().all())

    async def update(self, patient_id: int, data: PatientUpdate) -> PatientORM | None:
        patient = await self.get_by_id(patient_id)
        if not patient:
            return None
        update_data = data.model_dump(exclude_none=True)
        for key, value in update_data.items():
            setattr(patient, key, value)
        patient.updated_at = datetime.now()
        await self.session.flush()
        return patient

    async def delete(self, patient_id: int) -> bool:
        patient = await self.get_by_id(patient_id)
        if not patient:
            return False
        patient.is_active = False
        await self.session.flush()
        return True

    async def count(self) -> int:
        result = await self.session.execute(
            select(func.count()).where(PatientORM.is_active == True).select_from(PatientORM)
        )
        return result.scalar_one()
