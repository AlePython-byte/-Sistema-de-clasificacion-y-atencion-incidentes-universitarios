from fastapi import FastAPI

from app.api.incident_routes import router as incident_router
from app.core.config import settings


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API for managing and prioritizing university campus incidents.",
    version=settings.API_VERSION,
)

app.include_router(incident_router)


@app.get("/")
def read_root() -> dict[str, str]:
    """Return a basic API status message."""
    return {"message": "CampusCare API is running."}


@app.get("/health")
def health_check() -> dict[str, str]:
    """Return the service health status."""
    return {"status": "healthy"}
