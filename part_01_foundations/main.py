"""Part 1 — FastAPI application entry point."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from part_01_foundations.routers import ask, classify, health
from shared.config import get_settings
from shared.logger import logger

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown logic."""
    logger.info(f"Starting Hospital AI Platform — Part 1 | model={settings.llm_model}")
    logger.info(f"Environment: {settings.environment}")
    yield
    logger.info("Shutting down Part 1 application")


app = FastAPI(
    title="Hospital AI Platform — Part 1: Foundations",
    description=(
        "FastAPI + LangChain basics: async LLM endpoints, "
        "prompt templates, and LCEL chains."
    ),
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(ask.router)
app.include_router(classify.router)


@app.get("/")
async def root():
    return {
        "message": "Hospital AI Platform — Part 1",
        "docs": "/docs",
        "health": "/health",
    }
