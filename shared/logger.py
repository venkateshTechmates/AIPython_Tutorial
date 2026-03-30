"""Structured logging using loguru."""

import sys
from loguru import logger
from shared.config import get_settings


def configure_logging() -> None:
    settings = get_settings()
    logger.remove()

    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )

    logger.add(
        sys.stderr,
        format=log_format,
        level=settings.log_level,
        colorize=True,
        backtrace=True,
        diagnose=not settings.is_production,
    )

    if settings.is_production:
        logger.add(
            "logs/hospital_{time:YYYY-MM-DD}.log",
            rotation="1 day",
            retention="30 days",
            compression="zip",
            format=log_format,
            level="INFO",
            serialize=True,
        )


configure_logging()

__all__ = ["logger"]
