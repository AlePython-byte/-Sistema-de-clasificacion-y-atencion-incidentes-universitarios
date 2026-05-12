from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.incident_routes import router as incident_router
from app.core.config import settings
from app.schemas.error_schema import ErrorResponse


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API for managing and prioritizing university campus incidents.",
    version=settings.API_VERSION,
)

app.include_router(incident_router)


@app.exception_handler(HTTPException)
async def http_exception_handler(_request: Request, exc: HTTPException) -> JSONResponse:
    """Return a consistent response for HTTP errors."""
    error_response = ErrorResponse(
        detail=str(exc.detail),
        status_code=exc.status_code,
        error="HTTP_ERROR",
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.model_dump(),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    _request: Request,
    _exc: RequestValidationError,
) -> JSONResponse:
    """Return a consistent response for request validation errors."""
    error_response = ErrorResponse(
        detail="Validation error",
        status_code=422,
        error="VALIDATION_ERROR",
    )
    return JSONResponse(status_code=422, content=error_response.model_dump())


@app.get("/")
def read_root() -> dict[str, str]:
    """Return a basic API status message."""
    return {"message": "CampusCare API is running."}


@app.get("/health")
def health_check() -> dict[str, str]:
    """Return the service health status."""
    return {"status": "healthy"}
