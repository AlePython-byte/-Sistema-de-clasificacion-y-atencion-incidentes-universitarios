from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def build_incident_payload() -> dict[str, str]:
    return {
        "title": "Broken classroom projector",
        "description": "The projector in room B-204 does not turn on.",
        "category": "Technology",
        "location": "Building B, room 204",
        "reported_by": "student@example.edu",
        "urgency_level": "HIGH",
    }


def create_incident() -> dict:
    response = client.post("/api/incidents/", json=build_incident_payload())
    assert response.status_code == 201
    return response.json()


def test_create_incident_successfully() -> None:
    incident = create_incident()

    assert incident["title"] == "Broken classroom projector"
    assert incident["status"] == "OPEN"
    assert incident["priority"] == "HIGH"
    assert incident["assigned_to"] is None


def test_get_all_incidents_returns_created_incidents() -> None:
    created_incident = create_incident()

    response = client.get("/api/incidents/")

    assert response.status_code == 200
    assert any(incident["id"] == created_incident["id"] for incident in response.json())


def test_get_incident_by_id_returns_existing_incident() -> None:
    created_incident = create_incident()

    response = client.get(f"/api/incidents/{created_incident['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == created_incident["id"]


def test_get_incident_by_id_returns_404_when_missing() -> None:
    response = client.get("/api/incidents/non-existing-id")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Incident not found",
        "status_code": 404,
        "error": "HTTP_ERROR",
    }


def test_update_incident_status_successfully() -> None:
    created_incident = create_incident()

    response = client.patch(
        f"/api/incidents/{created_incident['id']}/status",
        json={"status": "IN_PROGRESS"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "IN_PROGRESS"


def test_assign_incident_successfully() -> None:
    created_incident = create_incident()

    response = client.patch(
        f"/api/incidents/{created_incident['id']}/assign",
        json={"assigned_to": "Maintenance Team"},
    )

    assert response.status_code == 200
    assert response.json()["assigned_to"] == "Maintenance Team"


def test_get_next_incident_returns_open_incident() -> None:
    created_incident = create_incident()

    response = client.get("/api/incidents/queue/next")

    assert response.status_code == 200
    assert response.json()["status"] == "OPEN"
    assert response.json()["id"] is not None
    assert created_incident["id"]


def test_create_incident_returns_422_when_payload_is_invalid() -> None:
    invalid_payload = build_incident_payload()
    invalid_payload["title"] = "Bad"

    response = client.post("/api/incidents/", json=invalid_payload)

    assert response.status_code == 422
    assert response.json() == {
        "detail": "Validation error",
        "status_code": 422,
        "error": "VALIDATION_ERROR",
    }
