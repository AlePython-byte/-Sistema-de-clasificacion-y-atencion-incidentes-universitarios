
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from fastapi import HTTPException

from app.repositories.incident_repository import IncidentRepository
from app.schemas.incident_schema import (
    IncidentAssignRequest,
    IncidentCreateRequest,
    IncidentResponse,
    IncidentStatus,
    IncidentUpdateStatusRequest,
)
from app.structures.history_stack import HistoryStack
from app.structures.priority_queue import PriorityQueueManager

# ── Mapa de transiciones permitidas ───────────────────────────────────────────
_VALID_TRANSITIONS: dict[IncidentStatus, set[IncidentStatus]] = {
    IncidentStatus.OPEN: {
        IncidentStatus.ASSIGNED,
        IncidentStatus.IN_PROGRESS,
        IncidentStatus.CLOSED,
    },
    IncidentStatus.ASSIGNED: {
        IncidentStatus.IN_PROGRESS,
        IncidentStatus.RESOLVED,
        IncidentStatus.CLOSED,
    },
    IncidentStatus.IN_PROGRESS: {
        IncidentStatus.RESOLVED,
        IncidentStatus.CLOSED,
    },
    IncidentStatus.RESOLVED: {
        IncidentStatus.CLOSED,
    },
    IncidentStatus.CLOSED: set(),  # estado terminal
}


class IncidentService:
    """Servicio principal de incidentes con reglas de negocio (Integrante 3)."""

    def __init__(self) -> None:
        self._repo = IncidentRepository()
        self._queue = PriorityQueueManager()
        self._history = HistoryStack()

    # ── Helpers privados ───────────────────────────────────────────────────────

    def _get_or_404(self, incident_id: str) -> dict:
        incident = self._repo.find_by_id(incident_id)
        if incident is None:
            raise HTTPException(status_code=404, detail="Incident not found")
        return incident

    def _validate_transition(
        self, current: IncidentStatus, new: IncidentStatus
    ) -> None:
        if current == IncidentStatus.CLOSED:
            raise HTTPException(
                status_code=422,
                detail="A CLOSED incident cannot change its status.",
            )
        if current == new:
            raise HTTPException(
                status_code=422,
                detail=f"Incident is already in status '{new}'.",
            )
        allowed = _VALID_TRANSITIONS.get(current, set())
        if new not in allowed:
            readable = [s.value for s in allowed] or ["none"]
            raise HTTPException(
                status_code=422,
                detail=(
                    f"Transition from '{current}' to '{new}' is not allowed. "
                    f"Valid next statuses: {readable}."
                ),
            )

    def _to_response(self, data: dict) -> IncidentResponse:
        """Convierte el dict del repositorio a IncidentResponse con historial."""
        data["history"] = self._history.get_history(data["id"])
        return IncidentResponse(**data)

    # ── Operaciones públicas ───────────────────────────────────────────────────

    def create_incident(self, request: IncidentCreateRequest) -> IncidentResponse:
        """Crea un incidente, lo inserta en la cola y registra su creación."""
        incident_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc)

        data: dict = {
            "id": incident_id,
            "title": request.title,
            "description": request.description,
            "category": request.category,
            "location": request.location,
            "reported_by": request.reported_by,
            "urgency_level": request.urgency_level,
            "status": IncidentStatus.OPEN,
            "assigned_to": request.assigned_to,
            "created_at": now,
            "history": [],
        }

        self._repo.save(data)
        self._queue.push(incident_id, request.urgency_level)

        self._history.push(
            incident_id,
            action="CREATED",
            detail=(
                f"Incident created with urgency '{request.urgency_level}' "
                f"by '{request.reported_by}'."
            ),
        )

        if request.assigned_to:
            self._history.push(
                incident_id,
                action="ASSIGNED",
                detail=f"Initial assignment to '{request.assigned_to}' at creation.",
            )

        return self._to_response(self._repo.find_by_id(incident_id))

    def get_all_incidents(self) -> list[IncidentResponse]:
        """Lista todos los incidentes con historial actualizado."""
        return [self._to_response(inc) for inc in self._repo.find_all()]

    def get_incident_by_id(self, incident_id: str) -> IncidentResponse:
        """Busca un incidente por ID."""
        return self._to_response(self._get_or_404(incident_id))

    def update_status(
        self, incident_id: str, request: IncidentUpdateStatusRequest
    ) -> IncidentResponse:
        """
        Cambia el estado del incidente aplicando las reglas de negocio.
        Registra el cambio en el historial y actualiza la cola si aplica.
        """
        incident = self._get_or_404(incident_id)
        current = IncidentStatus(incident["status"])
        new_status = request.status

        self._validate_transition(current, new_status)

        # Sacar de la cola si ya no está abierto
        if new_status != IncidentStatus.OPEN:
            self._queue.remove(incident_id)

        self._repo.update(incident_id, {"status": new_status})

        self._history.push(
            incident_id,
            action="STATUS_CHANGED",
            detail=f"Status changed from '{current}' to '{new_status}'.",
        )

        return self._to_response(self._repo.find_by_id(incident_id))

    def assign_incident(
        self, incident_id: str, request: IncidentAssignRequest
    ) -> IncidentResponse:
        """
        Asigna un responsable al incidente.
        • Solo en estado OPEN o ASSIGNED.
        • Si estaba OPEN pasa automáticamente a ASSIGNED.
        • Registra la asignación en el historial.
        """
        incident = self._get_or_404(incident_id)
        current = IncidentStatus(incident["status"])

        if current in (
            IncidentStatus.CLOSED,
            IncidentStatus.RESOLVED,
            IncidentStatus.IN_PROGRESS,
        ):
            raise HTTPException(
                status_code=422,
                detail=(
                    f"Cannot assign a responsible to an incident in status '{current}'. "
                    "Only OPEN or ASSIGNED incidents accept assignment."
                ),
            )

        previous_assignee = incident.get("assigned_to")
        updates: dict = {"assigned_to": request.assigned_to}

        # Cambio automático OPEN → ASSIGNED
        if current == IncidentStatus.OPEN:
            updates["status"] = IncidentStatus.ASSIGNED
            self._queue.remove(incident_id)
            self._history.push(
                incident_id,
                action="STATUS_CHANGED",
                detail="Status automatically changed from 'OPEN' to 'ASSIGNED' upon assignment.",
            )

        self._repo.update(incident_id, updates)

        detail = (
            f"Reassigned from '{previous_assignee}' to '{request.assigned_to}'."
            if previous_assignee
            else f"Assigned to '{request.assigned_to}' for the first time."
        )
        self._history.push(incident_id, action="ASSIGNED", detail=detail)

        return self._to_response(self._repo.find_by_id(incident_id))

    def get_next_incident(self) -> IncidentResponse:
        """
        Retorna el siguiente incidente OPEN de mayor prioridad.
        Prioridad: CRITICAL > HIGH > MEDIUM > LOW.
        """
        next_id = self._queue.peek()
        if not next_id:
            raise HTTPException(
                status_code=404,
                detail="No open incidents in the priority queue.",
            )
        incident = self._repo.find_by_id(next_id)
        if not incident:
            self._queue.remove(next_id)
            raise HTTPException(
                status_code=404,
                detail="No open incidents in the priority queue.",
            )
        return self._to_response(incident)