import type { PartData } from "../../types";

export const part03: PartData = {
  id: "03",
  title: "SQLite Persistence",
  goal: "Persist hospital data with SQLAlchemy 2.0 async ORM, async sessions, and Alembic migrations.",
  phase: 1,
  phaseLabel: "Core Foundations",
  folder: "part_03_sqlite",
  estimatedHours: 4,
  difficulty: "beginner",
  prerequisites: ["01", "02"],
  unlocks: ["04"],
  whatYouBuild: [
    { label: "POST /patients", description: "Create a new patient record" },
    { label: "GET /patients/{id}", description: "Retrieve patient by ID" },
    { label: "GET /patients", description: "List patients with pagination" },
    { label: "PUT /patients/{id}", description: "Update patient record" },
    { label: "POST /appointments", description: "Schedule an appointment" },
    { label: "GET /appointments/{id}", description: "Get appointment with doctor info" },
  ],
  mermaidDiagram: `
flowchart TD
  A[FastAPI Route] --> B[AsyncSession]
  B --> C[SQLAlchemy ORM]
  C --> D[(SQLite DB)]
  D --> C
  C --> B
  B --> A

  subgraph Models
    E[PatientORM]
    F[DoctorORM]
    G[AppointmentORM]
    H[InvoiceORM]
  end

  C -.->|uses| Models
  `,
  concepts: [
    {
      id: "async-engine",
      title: "SQLAlchemy Async Engine",
      explanation:
        "SQLAlchemy 2.0 supports async sessions via aiosqlite. The async_session factory creates context-managed database sessions.",
      code: {
        language: "python",
        filename: "shared/database.py",
        snippet: `from sqlalchemy.ext.asyncio import (
    create_async_engine, AsyncSession, async_sessionmaker
)
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine(
    "sqlite+aiosqlite:///hospital.db",
    echo=False
)

async_session = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

class Base(DeclarativeBase):
    pass

# Dependency injection for FastAPI
async def get_db():
    async with async_session() as session:
        yield session`,
      },
      glossaryTerms: ["SQLAlchemy", "Async Session"],
    },
    {
      id: "orm-models",
      title: "SQLAlchemy ORM Models",
      explanation:
        "ORM models map Python classes to database tables. Mapped[] typed columns enable full IDE support and type safety.",
      code: {
        language: "python",
        filename: "shared/database.py",
        snippet: `from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

class PatientORM(Base):
    __tablename__ = "patients"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True)
    date_of_birth: Mapped[datetime]
    blood_type: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow
    )

    appointments: Mapped[list["AppointmentORM"]] = relationship(
        back_populates="patient"
    )`,
      },
    },
    {
      id: "crud-operations",
      title: "Async CRUD Operations",
      explanation:
        "All database operations use async/await. SQLAlchemy's select() builds type-safe queries.",
      code: {
        language: "python",
        filename: "main.py",
        snippet: `from sqlalchemy import select

@app.get("/patients/{patient_id}")
async def get_patient(
    patient_id: str,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(PatientORM).where(PatientORM.id == patient_id)
    )
    patient = result.scalar_one_or_none()
    if not patient:
        raise HTTPException(404, "Patient not found")
    return patient`,
      },
    },
  ],
  steps: [
    {
      number: 1,
      title: "Define ORM models",
      description: "Create PatientORM, DoctorORM, AppointmentORM, InvoiceORM with relationships.",
    },
    {
      number: 2,
      title: "Create async engine and session factory",
      description: "Wire up aiosqlite async engine and async_sessionmaker.",
    },
    {
      number: 3,
      title: "Write CRUD functions",
      description: "Implement create, read, update, delete for patients and appointments.",
    },
    {
      number: 4,
      title: "Add FastAPI dependency injection",
      description: "Use Depends(get_db) to inject async sessions into route handlers.",
    },
    {
      number: 5,
      title: "Seed the database",
      description: "Load sample patients, doctors, and appointments from JSON fixtures.",
    },
  ],
  acceptanceCriteria: [
    { id: "ac1", text: "POST /patients creates record and returns it with 201" },
    { id: "ac2", text: "GET /patients/{id} returns 404 for unknown patient" },
    { id: "ac3", text: "GET /patients supports ?page=1&size=10 pagination" },
    { id: "ac4", text: "Database persists across server restarts" },
    { id: "ac5", text: "Appointment.doctor relationship is eagerly loaded" },
  ],
  gotchas: [
    {
      error: "MissingGreenlet: greenlet_spawn has not been called",
      cause: "Accessing lazy-loaded relationship outside async session",
      fix: "Use selectinload() or joinedload() when querying to eagerly load relationships",
    },
    {
      error: "sqlite3.OperationalError: no such table",
      cause: "Tables not created before first request",
      fix: "Call Base.metadata.create_all(engine) in lifespan startup",
    },
  ],
  resources: [
    { title: "SQLAlchemy 2.0 Async", url: "https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html" },
    { title: "FastAPI SQL Databases", url: "https://fastapi.tiangolo.com/tutorial/sql-databases/" },
  ],
};
