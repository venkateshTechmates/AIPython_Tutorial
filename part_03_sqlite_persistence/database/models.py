"""Part 3 — SQLAlchemy ORM models mapped to SQLite tables."""

from datetime import date, datetime
from sqlalchemy import Boolean, Date, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from shared.database.base import Base


class PatientORM(Base):
    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    patient_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    phone: Mapped[str] = mapped_column(String(30), nullable=False)
    address: Mapped[str] = mapped_column(String(500), nullable=False)
    blood_type: Mapped[str | None] = mapped_column(String(5), nullable=True)
    allergies: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON string
    emergency_contact_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    emergency_contact_phone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    insurance_provider: Mapped[str | None] = mapped_column(String(200), nullable=True)
    insurance_policy_number: Mapped[str | None] = mapped_column(String(100), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    appointments: Mapped[list["AppointmentORM"]] = relationship(
        "AppointmentORM", back_populates="patient", lazy="selectin"
    )


class DoctorORM(Base):
    __tablename__ = "doctors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    doctor_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    specialty: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    phone: Mapped[str] = mapped_column(String(30), nullable=False)
    license_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    department: Mapped[str] = mapped_column(String(100), nullable=False)
    years_of_experience: Mapped[int] = mapped_column(Integer, nullable=False)
    consultation_fee: Mapped[float] = mapped_column(Float, nullable=False)
    available_days: Mapped[str] = mapped_column(Text, nullable=False)  # JSON string
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    appointments: Mapped[list["AppointmentORM"]] = relationship(
        "AppointmentORM", back_populates="doctor", lazy="selectin"
    )


class AppointmentORM(Base):
    __tablename__ = "appointments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    appointment_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    patient_id: Mapped[int] = mapped_column(Integer, ForeignKey("patients.id"), nullable=False)
    doctor_id: Mapped[int] = mapped_column(Integer, ForeignKey("doctors.id"), nullable=False)
    scheduled_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    duration_minutes: Mapped[int] = mapped_column(Integer, default=30, nullable=False)
    reason: Mapped[str] = mapped_column(String(500), nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="scheduled", nullable=False)
    details_json: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    patient: Mapped["PatientORM"] = relationship("PatientORM", back_populates="appointments")
    doctor: Mapped["DoctorORM"] = relationship("DoctorORM", back_populates="appointments")
