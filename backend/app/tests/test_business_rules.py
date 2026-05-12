import pytest
from fastapi import HTTPException
from app.services.incident_service import IncidentService
from app.schemas.incident_schema import IncidentUpdateStatusRequest, IncidentStatus, IncidentCreateRequest, UrgencyLevel, IncidentAssignRequest
from app.repositories.incident_repository import IncidentRepository

@pytest.fixture
def service():
    return IncidentService(IncidentRepository())

def test_closed_cannot_return_to_open(service):
    request = IncidentCreateRequest(title="test", description="test desc", category="IT", location="B1", reported_by="user", urgency_level=UrgencyLevel.LOW)
    incident = service.create_incident(request)
    
    # move to closed
    service.update_status(incident.id, IncidentUpdateStatusRequest(status=IncidentStatus.CLOSED))
    
    with pytest.raises(HTTPException) as excinfo:
        service.update_status(incident.id, IncidentUpdateStatusRequest(status=IncidentStatus.OPEN))
    assert excinfo.value.status_code == 400
    assert "Cannot transition from CLOSED to OPEN" in excinfo.value.detail

def test_resolved_can_pass_to_closed(service):
    request = IncidentCreateRequest(title="test", description="test desc", category="IT", location="B1", reported_by="user", urgency_level=UrgencyLevel.LOW)
    incident = service.create_incident(request)
    
    # move to resolved
    service.update_status(incident.id, IncidentUpdateStatusRequest(status=IncidentStatus.RESOLVED))
    # move to closed
    res = service.update_status(incident.id, IncidentUpdateStatusRequest(status=IncidentStatus.CLOSED))
    assert res.status == IncidentStatus.CLOSED.value

def test_assigned_can_pass_to_in_progress(service):
    request = IncidentCreateRequest(title="test", description="test desc", category="IT", location="B1", reported_by="user", urgency_level=UrgencyLevel.LOW)
    incident = service.create_incident(request)
    
    # move to assigned
    service.update_status(incident.id, IncidentUpdateStatusRequest(status=IncidentStatus.ASSIGNED))
    # move to in progress
    res = service.update_status(incident.id, IncidentUpdateStatusRequest(status=IncidentStatus.IN_PROGRESS))
    assert res.status == IncidentStatus.IN_PROGRESS.value

def test_history_records_changes(service):
    request = IncidentCreateRequest(title="test", description="test desc", category="IT", location="B1", reported_by="user", urgency_level=UrgencyLevel.LOW)
    incident = service.create_incident(request)
    
    service.assign_incident(incident.id, IncidentAssignRequest(assigned_to="Dev"))
    history = service.history_stack.history.get(incident.id)
    assert len(history) >= 2 # open, assigned
    
def test_priority_queue(service):
    req_low = IncidentCreateRequest(title="low", description="desc", category="IT", location="B1", reported_by="user", urgency_level=UrgencyLevel.LOW)
    req_high = IncidentCreateRequest(title="high", description="desc", category="IT", location="B1", reported_by="user", urgency_level=UrgencyLevel.HIGH)
    
    service.create_incident(req_low)
    high_inc = service.create_incident(req_high)
    
    next_inc = service.get_next_incident()
    assert next_inc.id == high_inc.id
