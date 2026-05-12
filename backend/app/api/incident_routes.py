from fastapi import APIRouter

from app.schemas.incident_schema import (
    IncidentAssignRequest,
    IncidentCreateRequest,
    IncidentResponse,
    IncidentUpdateStatusRequest,
)
from app.services.incident_service import IncidentService


router = APIRouter(prefix="/api/incidents", tags=["Incidents"])
incident_service = IncidentService()


@router.post("/", response_model=IncidentResponse, status_code=201)
def create_incident(request: IncidentCreateRequest) -> IncidentResponse:
    """Create a new campus incident."""
    return incident_service.create_incident(request)


@router.get("/", response_model=list[IncidentResponse])
def get_all_incidents() -> list[IncidentResponse]:
    """List all registered incidents."""
    return incident_service.get_all_incidents()


@router.get("/queue/next", response_model=IncidentResponse | None)
def get_next_incident() -> IncidentResponse | None:
    """Return the next open incident to attend."""
    return incident_service.get_next_incident()


@router.get("/{incident_id}", response_model=IncidentResponse)
def get_incident_by_id(incident_id: str) -> IncidentResponse:
    """Find an incident by its unique identifier."""
    return incident_service.get_incident_by_id(incident_id)


@router.patch("/{incident_id}/status", response_model=IncidentResponse)
def update_incident_status(
    incident_id: str,
    request: IncidentUpdateStatusRequest,
) -> IncidentResponse:
    """Update the current status of an incident."""
    return incident_service.update_status(incident_id, request)


@router.patch("/{incident_id}/assign", response_model=IncidentResponse)
def assign_incident(
    incident_id: str,
    request: IncidentAssignRequest,
) -> IncidentResponse:
    """Assign an incident to a responsible person or team."""
    return incident_service.assign_incident(incident_id, request)
