"""Part 3 — FastAPI app with DB-backed endpoints."""

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends, status

from part_03_sqlite_persistence.database.base import init_tables
from part_03_sqlite_persistence.dependencies import (
    get_patient_repo,
    get_doctor_repo,
    get_appointment_repo,
)
from part_03_sqlite_persistence.repositories.patient_repo import PatientRepository
from part_03_sqlite_persistence.repositories.doctor_repo import DoctorRepository
from part_03_sqlite_persistence.repositories.appointment_repo import AppointmentRepository
from shared.models.patient import PatientCreate, PatientUpdate
from shared.models.doctor import DoctorCreate
from shared.models.appointment import AppointmentCreate, AppointmentStatus
from shared.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing database tables...")
    await init_tables()
    logger.info("Part 3 — SQLite Persistence app ready")
    yield
    logger.info("Shutting down Part 3 app")


app = FastAPI(
    title="Hospital AI Platform — Part 3: SQLite Persistence",
    description="Async SQLAlchemy 2.0 + SQLite with repository pattern.",
    version="1.0.0",
    lifespan=lifespan,
)


# ── Patients ──────────────────────────────────────────────────────────────────

@app.post("/patients", status_code=status.HTTP_201_CREATED)
async def create_patient(
    data: PatientCreate,
    repo: PatientRepository = Depends(get_patient_repo),
):
    return await repo.create(data)


@app.get("/patients")
async def list_patients(
    offset: int = 0,
    limit: int = 50,
    repo: PatientRepository = Depends(get_patient_repo),
):
    return await repo.get_all(offset=offset, limit=limit)


@app.get("/patients/{patient_id}")
async def get_patient(
    patient_id: int,
    repo: PatientRepository = Depends(get_patient_repo),
):
    patient = await repo.get_by_id(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@app.patch("/patients/{patient_id}")
async def update_patient(
    patient_id: int,
    data: PatientUpdate,
    repo: PatientRepository = Depends(get_patient_repo),
):
    patient = await repo.update(patient_id, data)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@app.delete("/patients/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_patient(
    patient_id: int,
    repo: PatientRepository = Depends(get_patient_repo),
):
    deleted = await repo.delete(patient_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Patient not found")


# ── Doctors ───────────────────────────────────────────────────────────────────

@app.post("/doctors", status_code=status.HTTP_201_CREATED)
async def create_doctor(
    data: DoctorCreate,
    repo: DoctorRepository = Depends(get_doctor_repo),
):
    return await repo.create(data)


@app.get("/doctors")
async def list_doctors(repo: DoctorRepository = Depends(get_doctor_repo)):
    return await repo.get_all()


@app.get("/doctors/{doctor_id}")
async def get_doctor(
    doctor_id: int,
    repo: DoctorRepository = Depends(get_doctor_repo),
):
    doctor = await repo.get_by_id(doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor


# ── Appointments ──────────────────────────────────────────────────────────────

@app.post("/appointments", status_code=status.HTTP_201_CREATED)
async def create_appointment(
    data: AppointmentCreate,
    repo: AppointmentRepository = Depends(get_appointment_repo),
):
    return await repo.create(data)


@app.get("/appointments/{appointment_id}")
async def get_appointment(
    appointment_id: int,
    repo: AppointmentRepository = Depends(get_appointment_repo),
):
    appt = await repo.get_by_id(appointment_id)
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appt


@app.get("/patients/{patient_id}/appointments")
async def get_patient_appointments(
    patient_id: int,
    repo: AppointmentRepository = Depends(get_appointment_repo),
):
    return await repo.get_by_patient(patient_id)


@app.patch("/appointments/{appointment_id}/status")
async def update_appointment_status(
    appointment_id: int,
    new_status: AppointmentStatus,
    repo: AppointmentRepository = Depends(get_appointment_repo),
):
    appt = await repo.update_status(appointment_id, new_status)
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appt


@app.get("/health")
async def health():
    return {"status": "healthy", "part": 3}
