from fastapi.testclient import TestClient

from app.api.incident_routes import incident_service
from app.main import app
from app.repositories.incident_repository import IncidentRepository
from app.structures.history_stack import IncidentHistoryStack


client = TestClient(app)


def setup_function() -> None:
    incident_service.repository = IncidentRepository()
    incident_service.history_stack = IncidentHistoryStack()


def build_incident_payload(urgency_level: str = "HIGH") -> dict[str, str]:
    return {
        "title": f"{urgency_level.title()} campus incident",
        "description": "This incident is used to validate business rules.",
        "category": "Technology",
        "location": "Building A",
        "reported_by": "qa@example.edu",
        "urgency_level": urgency_level,
    }


def create_incident(urgency_level: str = "HIGH") -> dict:
    response = client.post("/api/incidents/", json=build_incident_payload(urgency_level))
    assert response.status_code == 201
    return response.json()


def test_get_next_incident_returns_critical_before_other_priorities() -> None:
    create_incident("LOW")
    critical_incident = create_incident("CRITICAL")
    create_incident("HIGH")
    create_incident("MEDIUM")

    response = client.get("/api/incidents/queue/next")

    assert response.status_code == 200
    assert response.json()["id"] == critical_incident["id"]
    assert response.json()["priority"] == "CRITICAL"


def test_get_next_incident_returns_high_before_low() -> None:
    create_incident("LOW")
    high_incident = create_incident("HIGH")

    response = client.get("/api/incidents/queue/next")

    assert response.status_code == 200
    assert response.json()["id"] == high_incident["id"]
    assert response.json()["priority"] == "HIGH"


def test_get_next_incident_returns_none_when_no_open_incidents_exist() -> None:
    response = client.get("/api/incidents/queue/next")

    assert response.status_code == 200
    assert response.json() is None


def test_assign_incident_changes_open_status_to_assigned() -> None:
    incident = create_incident()

    response = client.patch(
        f"/api/incidents/{incident['id']}/assign",
        json={"assigned_to": "Support Team"},
    )

    assert response.status_code == 200
    assert response.json()["assigned_to"] == "Support Team"
    assert response.json()["status"] == "ASSIGNED"


def test_cannot_assign_closed_incident() -> None:
    incident = create_incident()
    client.patch(f"/api/incidents/{incident['id']}/status", json={"status": "CLOSED"})

    response = client.patch(
        f"/api/incidents/{incident['id']}/assign",
        json={"assigned_to": "Support Team"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Closed incidents cannot be assigned."


def test_cannot_change_closed_incident_to_open() -> None:
    incident = create_incident()
    client.patch(f"/api/incidents/{incident['id']}/status", json={"status": "CLOSED"})

    response = client.patch(
        f"/api/incidents/{incident['id']}/status",
        json={"status": "OPEN"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Closed incidents cannot be reopened."


def test_resolved_incident_can_be_closed() -> None:
    incident = create_incident()
    client.patch(f"/api/incidents/{incident['id']}/status", json={"status": "RESOLVED"})

    response = client.patch(
        f"/api/incidents/{incident['id']}/status",
        json={"status": "CLOSED"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "CLOSED"


def test_update_status_for_missing_incident_returns_404() -> None:
    response = client.patch(
        "/api/incidents/missing-id/status",
        json={"status": "IN_PROGRESS"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Incident not found"


def test_assign_missing_incident_returns_404() -> None:
    response = client.patch(
        "/api/incidents/missing-id/assign",
        json={"assigned_to": "Support Team"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Incident not found"


def test_history_is_recorded_when_incident_is_created() -> None:
    incident = create_incident()

    history = incident_service.get_incident_history(incident["id"])

    assert len(history) == 1
    assert history[0]["action"] == "INCIDENT_CREATED"
    assert history[0]["previous_value"] is None
    assert history[0]["new_value"] == "OPEN"


def test_history_is_recorded_when_incident_is_assigned() -> None:
    incident = create_incident()

    client.patch(
        f"/api/incidents/{incident['id']}/assign",
        json={"assigned_to": "Support Team"},
    )
    history = incident_service.get_incident_history(incident["id"])

    assert [event["action"] for event in history] == [
        "INCIDENT_CREATED",
        "INCIDENT_ASSIGNED",
    ]
    assert history[-1]["previous_value"] is None
    assert history[-1]["new_value"] == "Support Team"


def test_history_is_recorded_when_status_changes() -> None:
    incident = create_incident()

    client.patch(
        f"/api/incidents/{incident['id']}/status",
        json={"status": "IN_PROGRESS"},
    )
    history = incident_service.get_incident_history(incident["id"])

    assert history[-1]["action"] == "STATUS_CHANGED"
    assert history[-1]["previous_value"] == "OPEN"
    assert history[-1]["new_value"] == "IN_PROGRESS"
