from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException

from app.repositories.incident_repository import IncidentRepository
from app.schemas.incident_schema import (
    IncidentAssignRequest,
    IncidentCreateRequest,
    IncidentResponse,
    IncidentUpdateStatusRequest,
    IncidentStatus,
    UrgencyLevel,
)
from app.structures.priority_queue import PriorityQueueManager
from app.structures.history_stack import IncidentHistoryStack


class IncidentService:
    def __init__(self, repository: IncidentRepository | None = None) -> None:
        self.repository = repository or IncidentRepository()
        self.queue_manager = PriorityQueueManager()
        self.history_stack = IncidentHistoryStack()

    def create_incident(self, request: IncidentCreateRequest) -> IncidentResponse:
        incident = {
            "id": str(uuid4()),
            "title": request.title,
            "description": request.description,
            "category": request.category,
            "location": request.location,
            "reported_by": request.reported_by,
            "urgency_level": request.urgency_level.value,
            "priority": self._calculate_priority(request.urgency_level),
            "status": IncidentStatus.OPEN.value,
            "assigned_to": None,
            "created_at": datetime.now(timezone.utc),
        }

        saved_incident = self.repository.save(incident)
        self.history_stack.push(saved_incident["id"], None, IncidentStatus.OPEN.value, "status")
        return IncidentResponse(**saved_incident)

    def get_all_incidents(self) -> list[IncidentResponse]:
        return [IncidentResponse(**incident) for incident in self.repository.find_all()]

    def get_incident_by_id(self, incident_id: str) -> IncidentResponse:
        return IncidentResponse(**self._get_existing_incident(incident_id))

    def update_status(
        self,
        incident_id: str,
        request: IncidentUpdateStatusRequest,
    ) -> IncidentResponse:
        incident = self._get_existing_incident(incident_id)
        current_status = incident["status"]
        new_status = request.status.value

        # Business rules
        if current_status == IncidentStatus.CLOSED.value and new_status == IncidentStatus.OPEN.value:
            raise HTTPException(status_code=400, detail="Cannot transition from CLOSED to OPEN")

        if current_status == IncidentStatus.RESOLVED.value and new_status not in [IncidentStatus.CLOSED.value]:
            raise HTTPException(status_code=400, detail="RESOLVED can only transition to CLOSED")

        if current_status == IncidentStatus.ASSIGNED.value and new_status not in [IncidentStatus.IN_PROGRESS.value, IncidentStatus.CLOSED.value]:
            raise HTTPException(status_code=400, detail="ASSIGNED can typically transition to IN_PROGRESS")

        updated_incident = self.repository.update(
            incident_id,
            {"status": new_status},
        )
        self.history_stack.push(incident_id, current_status, new_status, "status")
        return IncidentResponse(**self._ensure_updated(updated_incident))

    def assign_incident(
        self,
        incident_id: str,
        request: IncidentAssignRequest,
    ) -> IncidentResponse:
        incident = self._get_existing_incident(incident_id)
        old_assigned = incident.get("assigned_to")
        
        # When assigned, typically changes status to ASSIGNED if OPEN
        updated_data = {"assigned_to": request.assigned_to}
        if incident["status"] == IncidentStatus.OPEN.value:
            updated_data["status"] = IncidentStatus.ASSIGNED.value
            self.history_stack.push(incident_id, IncidentStatus.OPEN.value, IncidentStatus.ASSIGNED.value, "status")

        updated_incident = self.repository.update(
            incident_id,
            updated_data,
        )
        self.history_stack.push(incident_id, old_assigned, request.assigned_to, "assignment")
        return IncidentResponse(**self._ensure_updated(updated_incident))

    def get_next_incident(self) -> IncidentResponse | None:
        # Fetch all open incidents and put them into the PriorityQueue
        self.queue_manager = PriorityQueueManager()
        for incident in self.repository.find_all():
            if incident["status"] == IncidentStatus.OPEN.value:
                self.queue_manager.add(incident)
                
        next_incident = self.queue_manager.get_next()
        if next_incident:
            return IncidentResponse(**next_incident)

        return None

    def _get_existing_incident(self, incident_id: str) -> dict:
        incident = self.repository.find_by_id(incident_id)
        if incident is None:
            raise HTTPException(status_code=404, detail="Incident not found")

        return incident

    def _ensure_updated(self, incident: dict | None) -> dict:
        if incident is None:
            raise HTTPException(status_code=404, detail="Incident not found")

        return incident

    def _calculate_priority(self, urgency_level: UrgencyLevel) -> str:
        return urgency_level.value
