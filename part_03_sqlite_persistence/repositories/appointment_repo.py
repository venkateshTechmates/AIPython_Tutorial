"""Part 3 — Appointment repository (CRUD)."""

import json
from datetime import datetime
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from part_03_sqlite_persistence.database.models import AppointmentORM
from shared.models.appointment import AppointmentCreate, AppointmentStatus


def _generate_appointment_number(appt_id: int) -> str:
    return f"APT-{appt_id:05d}"


class AppointmentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, data: AppointmentCreate) -> AppointmentORM:
        appointment = AppointmentORM(
            appointment_number="APT-TEMP",
            patient_id=data.patient_id,
            doctor_id=data.doctor_id,
            scheduled_at=data.scheduled_at,
            duration_minutes=data.duration_minutes,
            reason=data.reason,
            notes=data.notes,
            details_json=data.details.model_dump_json() if data.details else None,
        )
        self.session.add(appointment)
        await self.session.flush()
        appointment.appointment_number = _generate_appointment_number(appointment.id)
        await self.session.flush()
        return appointment

    async def get_by_id(self, appointment_id: int) -> AppointmentORM | None:
        result = await self.session.execute(
            select(AppointmentORM).where(AppointmentORM.id == appointment_id)
        )
        return result.scalar_one_or_none()

    async def get_by_patient(self, patient_id: int) -> list[AppointmentORM]:
        result = await self.session.execute(
            select(AppointmentORM)
            .where(AppointmentORM.patient_id == patient_id)
            .order_by(AppointmentORM.scheduled_at.desc())
        )
        return list(result.scalars().all())

    async def get_by_doctor(self, doctor_id: int) -> list[AppointmentORM]:
        result = await self.session.execute(
            select(AppointmentORM)
            .where(AppointmentORM.doctor_id == doctor_id)
            .order_by(AppointmentORM.scheduled_at)
        )
        return list(result.scalars().all())

    async def update_status(
        self, appointment_id: int, status: AppointmentStatus
    ) -> AppointmentORM | None:
        appt = await self.get_by_id(appointment_id)
        if not appt:
            return None
        appt.status = status.value
        appt.updated_at = datetime.now()
        await self.session.flush()
        return appt

    async def count(self) -> int:
        result = await self.session.execute(
            select(func.count()).select_from(AppointmentORM)
        )
        return result.scalar_one()
