from typing import List

from app.clients.api_client import ApiClient
from app.models.incident_view_model import IncidentViewModel


class IncidentFrontendService:
    def __init__(self, api_client: ApiClient):
        self.api = api_client

    def load_incidents(self) -> List[IncidentViewModel]:
        raw = self.api.get_incidents()
        incidents = []
        for item in raw:
            incidents.append(IncidentViewModel(
                incident_id=item.get('id'),
                title=item.get('title', ''),
                description=item.get('description', ''),
                category=item.get('category', ''),
                location=item.get('location', ''),
                priority=item.get('priority', 'Normal'),
                status=item.get('status', 'Unknown')
            ))
        return incidents

    def register_incident(self, title: str, description: str, category: str, location: str) -> IncidentViewModel:
        payload = {
            'title': title,
            'description': description,
            'category': category,
            'location': location
        }
        created = self.api.create_incident(payload)
        return IncidentViewModel(
            incident_id=created.get('id'),
            title=created.get('title'),
            description=created.get('description'),
            category=created.get('category'),
            location=created.get('location'),
            priority=created.get('priority', 'Normal'),
            status=created.get('status', 'Open')
        )

    def load_next_incident(self) -> IncidentViewModel:
        item = self.api.get_next_incident()
        return IncidentViewModel(
            incident_id=item.get('id'),
            title=item.get('title'),
            description=item.get('description'),
            category=item.get('category'),
            location=item.get('location'),
            priority=item.get('priority', 'Normal'),
            status=item.get('status', 'Pending')
        )

    def load_report_summary(self) -> dict:
        return self.api.get_reports()
