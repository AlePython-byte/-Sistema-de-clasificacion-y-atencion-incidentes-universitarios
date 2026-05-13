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
from app.structures.history_stack import IncidentHistoryStack
from app.structures.priority_queue import PriorityQueueManager


class IncidentService:
    def __init__(
        self,
        repository: IncidentRepository | None = None,
        history_stack: IncidentHistoryStack | None = None,
    ) -> None:
        self.repository = repository or IncidentRepository()
        self.history_stack = history_stack or IncidentHistoryStack()

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
        self._record_history(
            incident_id=saved_incident["id"],
            action="INCIDENT_CREATED",
            previous_value=None,
            new_value=saved_incident["status"],
        )
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
        current_incident = self._get_existing_incident(incident_id)
        previous_status = current_incident["status"]
        new_status = request.status.value

        if previous_status == IncidentStatus.CLOSED.value and new_status == IncidentStatus.OPEN.value:
            raise HTTPException(
                status_code=400,
                detail="Closed incidents cannot be reopened.",
            )

        updated_incident = self.repository.update(
            incident_id,
            {"status": new_status},
        )
        updated_incident = self._ensure_updated(updated_incident)
        self._record_history(
            incident_id=incident_id,
            action="STATUS_CHANGED",
            previous_value=previous_status,
            new_value=new_status,
        )
        return IncidentResponse(**updated_incident)

    def assign_incident(
        self,
        incident_id: str,
        request: IncidentAssignRequest,
    ) -> IncidentResponse:
        current_incident = self._get_existing_incident(incident_id)
        if current_incident["status"] == IncidentStatus.CLOSED.value:
            raise HTTPException(
                status_code=400,
                detail="Closed incidents cannot be assigned.",
            )

        if request.assigned_to is None or not request.assigned_to.strip():
            raise HTTPException(
                status_code=400,
                detail="Assigned person or team cannot be empty.",
            )

        previous_value = current_incident.get("assigned_to")
        updated_data = {"assigned_to": request.assigned_to}
        if current_incident["status"] == IncidentStatus.OPEN.value:
            updated_data["status"] = IncidentStatus.ASSIGNED.value

        updated_incident = self.repository.update(
            incident_id,
            updated_data,
        )
        updated_incident = self._ensure_updated(updated_incident)
        self._record_history(
            incident_id=incident_id,
            action="INCIDENT_ASSIGNED",
            previous_value=previous_value,
            new_value=request.assigned_to,
        )
        return IncidentResponse(**updated_incident)

    def get_next_incident(self) -> IncidentResponse | None:
        priority_queue = PriorityQueueManager()
        for incident in self.repository.find_all():
            if incident["status"] == IncidentStatus.OPEN.value:
                priority_queue.add_incident(incident)

        next_incident = priority_queue.get_next_incident()
        if next_incident is None:
            return None

        return IncidentResponse(**next_incident)

    def get_incident_history(self, incident_id: str) -> list[dict]:
        return [
            event
            for event in self.history_stack.get_events()
            if event["incident_id"] == incident_id
        ]

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

    def _record_history(
        self,
        incident_id: str,
        action: str,
        previous_value: str | None,
        new_value: str | None,
    ) -> None:
        self.history_stack.push_event(
            {
                "incident_id": incident_id,
                "action": action,
                "previous_value": previous_value,
                "new_value": new_value,
                "created_at": datetime.now(timezone.utc),
            }
        )
