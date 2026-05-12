from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException

from app.repositories.incident_repository import IncidentRepository
from app.schemas.incident_schema import (
    IncidentAssignRequest,
    IncidentCreateRequest,
    IncidentResponse,
    IncidentUpdateStatusRequest,
)


class IncidentService:
    def __init__(self, repository: IncidentRepository | None = None) -> None:
        self.repository = repository or IncidentRepository()

    def create_incident(self, request: IncidentCreateRequest) -> IncidentResponse:
        incident = {
            "id": str(uuid4()),
            "title": request.title,
            "description": request.description,
            "category": request.category,
            "location": request.location,
            "reported_by": request.reported_by,
            "urgency_level": request.urgency_level,
            "priority": self._calculate_priority(request.urgency_level),
            "status": "OPEN",
            "assigned_to": None,
            "created_at": datetime.now(timezone.utc),
        }

        saved_incident = self.repository.save(incident)
        return IncidentResponse(**saved_incident)

    def get_all_incidents(self) -> list[IncidentResponse]:
        return [IncidentResponse(**incident) for incident in self.repository.find_all()]

    def get_incident_by_id(self, incident_id: str) -> IncidentResponse:
        incident = self.repository.find_by_id(incident_id)
        if incident is None:
            raise HTTPException(status_code=404, detail="Incident not found.")

        return IncidentResponse(**incident)

    def update_status(
        self,
        incident_id: str,
        request: IncidentUpdateStatusRequest,
    ) -> IncidentResponse:
        updated_incident = self.repository.update(
            incident_id,
            {"status": request.status},
        )
        if updated_incident is None:
            raise HTTPException(status_code=404, detail="Incident not found.")

        return IncidentResponse(**updated_incident)

    def assign_incident(
        self,
        incident_id: str,
        request: IncidentAssignRequest,
    ) -> IncidentResponse:
        updated_incident = self.repository.update(
            incident_id,
            {"assigned_to": request.assigned_to},
        )
        if updated_incident is None:
            raise HTTPException(status_code=404, detail="Incident not found.")

        return IncidentResponse(**updated_incident)

    def get_next_incident(self) -> IncidentResponse | None:
        # TODO: Integrate PriorityQueueManager from Team Member 2.
        for incident in self.repository.find_all():
            if incident["status"] == "OPEN":
                return IncidentResponse(**incident)

        return None

    def _calculate_priority(self, urgency_level: str) -> str:
        return urgency_level
