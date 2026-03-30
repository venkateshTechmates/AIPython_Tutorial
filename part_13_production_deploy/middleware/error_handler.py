"""Part 13 — Global error handler for FastAPI."""

import traceback
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException


async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "path": str(request.url.path),
        },
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    errors = []
    for error in exc.errors():
        errors.append({
            "field": " → ".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"],
        })
    return JSONResponse(
        status_code=422,
        content={"error": "Validation error", "details": errors},
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    # Log full traceback server-side but never expose it to the client
    tb = traceback.format_exc()
    # In production, ship this to your logging/alerting system
    print(f"Unhandled error on {request.method} {request.url}: {tb}")
    return JSONResponse(
        status_code=500,
        content={"error": "An internal server error occurred. Please try again later."},
    )
