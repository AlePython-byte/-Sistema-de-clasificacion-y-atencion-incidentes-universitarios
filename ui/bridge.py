import sys
import os
from typing import List, Optional, Any

# Ensure the backend directory is in sys.path
# File is in project_root/ui/bridge.py
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
backend_path = os.path.join(project_root, "backend")

if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# Fallback classes for type hinting and safety
class IncidentResponse: id: str; title: str; description: str; category: str; location: str; reported_by: str; priority: str; status: str; created_at: Any
class IncidentService: pass

try:
    from app.services.incident_service import IncidentService
    from app.schemas.incident_schema import (
        IncidentCreateRequest,
        IncidentResponse,
        IncidentUpdateStatusRequest,
        IncidentAssignRequest,
        UrgencyLevel,
        IncidentStatus
    )
    from fastapi import HTTPException
except ImportError as e:
    print(f"DEBUG: Backend Import Error: {e}")
    # Initialize basic types to avoid NameError if backend is missing
    IncidentCreateRequest = Any
    IncidentUpdateStatusRequest = Any
    IncidentAssignRequest = Any
    UrgencyLevel = Any
    IncidentStatus = Any
    HTTPException = Exception



class BackendBridge:
    """
    Adapter layer between the CustomTkinter UI and the FastAPI Backend Service.
    Handles data transformation and exception mapping.
    """
    
    def __init__(self):
        self._service = IncidentService()
        self._on_log_callback = None

    def set_log_callback(self, callback):
        """Sets a callback to send logs to the UI console."""
        self._on_log_callback = callback

    def _log(self, message: str, level: str = "INFO"):
        if self._on_log_callback:
            self._on_log_callback(f"[{level}] {message}")

    def create_incident(self, data: dict) -> Optional[IncidentResponse]:
        try:
            self._log(f"Attempting to create incident: {data.get('title')}")
            request = IncidentCreateRequest(**data)
            response = self._service.create_incident(request)
            self._log(f"Incident created successfully with ID: {response.id}")
            return response
        except Exception as e:
            self._log(f"Failed to create incident: {str(e)}", "ERROR")
            return None

    def get_all_incidents(self) -> List[IncidentResponse]:
        try:
            incidents = self._service.get_all_incidents()
            self._log(f"Fetched {len(incidents)} incidents from backend.")
            return incidents
        except Exception as e:
            self._log(f"Failed to fetch incidents: {str(e)}", "ERROR")
            return []

    def update_incident_status(self, incident_id: str, status: str) -> Optional[IncidentResponse]:
        try:
            self._log(f"Updating incident {incident_id} status to {status}")
            request = IncidentUpdateStatusRequest(status=status)
            response = self._service.update_status(incident_id, request)
            self._log(f"Status updated for incident {incident_id}")
            return response
        except HTTPException as e:
            self._log(f"Backend error: {e.detail}", "WARNING")
            return None
        except Exception as e:
            self._log(f"Critical error updating status: {str(e)}", "ERROR")
            return None

    def assign_incident(self, incident_id: str, assigned_to: str) -> Optional[IncidentResponse]:
        try:
            self._log(f"Assigning incident {incident_id} to {assigned_to}")
            request = IncidentAssignRequest(assigned_to=assigned_to)
            response = self._service.assign_incident(incident_id, request)
            self._log(f"Incident {incident_id} assigned successfully.")
            return response
        except Exception as e:
            self._log(f"Failed to assign incident: {str(e)}", "ERROR")
            return None
