from fastapi import APIRouter

from app.schemas.incident_schema import (
    IncidentAssignRequest,
    IncidentCreateRequest,
    IncidentResponse,
    IncidentUpdateStatusRequest,
)
from app.schemas.error_schema import ErrorResponse
from app.services.incident_service import IncidentService


router = APIRouter(prefix="/api/incidents", tags=["Incidents"])
incident_service = IncidentService()

NOT_FOUND_RESPONSE = {404: {"model": ErrorResponse, "description": "Incident not found"}}
VALIDATION_RESPONSE = {422: {"model": ErrorResponse, "description": "Validation error"}}
ERROR_RESPONSES = {**NOT_FOUND_RESPONSE, **VALIDATION_RESPONSE}


@router.post(
    "/",
    response_model=IncidentResponse,
    status_code=201,
    summary="Create incident",
    description="Register a new campus incident with initial OPEN status and priority based on urgency.",
    responses=VALIDATION_RESPONSE,
)
def create_incident(request: IncidentCreateRequest) -> IncidentResponse:
    """Create a new campus incident."""
    return incident_service.create_incident(request)


@router.get(
    "/",
    response_model=list[IncidentResponse],
    summary="List incidents",
    description="Return all incidents currently stored in the in-memory repository.",
)
def get_all_incidents() -> list[IncidentResponse]:
    """List all registered incidents."""
    return incident_service.get_all_incidents()


@router.get(
    "/queue/next",
    response_model=IncidentResponse | None,
    summary="Get next incident",
    description=(
        "Return the first open incident found. This is a temporary implementation "
        "until PriorityQueueManager is integrated by Team Member 2."
    ),
)
def get_next_incident() -> IncidentResponse | None:
    """Return the next open incident to attend."""
    return incident_service.get_next_incident()


@router.get(
    "/{incident_id}",
    response_model=IncidentResponse,
    summary="Get incident by ID",
    description="Find one incident using its unique identifier.",
    responses=NOT_FOUND_RESPONSE,
)
def get_incident_by_id(incident_id: str) -> IncidentResponse:
    """Find an incident by its unique identifier."""
    return incident_service.get_incident_by_id(incident_id)


@router.patch(
    "/{incident_id}/status",
    response_model=IncidentResponse,
    summary="Update incident status",
    description="Update the lifecycle status of an existing incident.",
    responses=ERROR_RESPONSES,
)
def update_incident_status(
    incident_id: str,
    request: IncidentUpdateStatusRequest,
) -> IncidentResponse:
    """Update the current status of an incident."""
    return incident_service.update_status(incident_id, request)


@router.patch(
    "/{incident_id}/assign",
    response_model=IncidentResponse,
    summary="Assign incident",
    description="Assign an existing incident to a responsible person or team.",
    responses=ERROR_RESPONSES,
)
def assign_incident(
    incident_id: str,
    request: IncidentAssignRequest,
) -> IncidentResponse:
    """Assign an incident to a responsible person or team."""
    return incident_service.assign_incident(incident_id, request)
