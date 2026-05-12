class IncidentRepository:
    def __init__(self) -> None:
        self._incidents: dict[str, dict] = {}

    def save(self, incident: dict) -> dict:
        self._incidents[incident["id"]] = incident
        return incident

    def find_all(self) -> list[dict]:
        return list(self._incidents.values())

    def find_by_id(self, incident_id: str) -> dict | None:
        return self._incidents.get(incident_id)

    def update(self, incident_id: str, updated_data: dict) -> dict | None:
        incident = self.find_by_id(incident_id)
        if incident is None:
            return None

        incident.update(updated_data)
        return incident
