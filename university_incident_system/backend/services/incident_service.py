from backend.services.classification_service import ClassificationService
from backend.services.assignment_service import AssignmentService
from backend.business.priority_rules import PriorityRules
from backend.business.incident_status_rules import IncidentStatusRules


class IncidentService:
    """
    Main service responsible for managing incidents.
    """

    def __init__(self):
        self.classification_service = ClassificationService()
        self.assignment_service = AssignmentService()
        self.priority_rules = PriorityRules()
        self.status_rules = IncidentStatusRules()
        self.incidents = []
        self.next_id = 1

    def create_incident(self, title: str, description: str, location: str, reporter_name: str) -> dict:
        category = self.classification_service.classify_incident(description)
        priority = self.priority_rules.calculate_priority(category, description)
        assigned_department = self.assignment_service.assign_department(category)

        incident = {
            "id": self.next_id,
            "title": title,
            "description": description,
            "location": location,
            "reporter_name": reporter_name,
            "category": category,
            "priority": priority,
            "assigned_department": assigned_department,
            "status": "Pendiente"
        }

        self.incidents.append(incident)
        self.next_id += 1

        return incident

    def get_all_incidents(self) -> list:
        return self.incidents

    def get_incident_by_id(self, incident_id: int) -> dict | None:
        for incident in self.incidents:
            if incident["id"] == incident_id:
                return incident

        return None

    def update_status(self, incident_id: int, new_status: str) -> bool:
        incident = self.get_incident_by_id(incident_id)

        if incident is None:
            return False

        current_status = incident["status"]

        if not self.status_rules.can_change_status(current_status, new_status):
            return False

        incident["status"] = new_status
        return True

    def get_incidents_by_priority(self, priority: str) -> list:
        return [
            incident for incident in self.incidents
            if incident["priority"] == priority
        ]

    def get_incidents_by_department(self, department: str) -> list:
        return [
            incident for incident in self.incidents
            if incident["assigned_department"] == department
        ]

    def get_incidents_by_status(self, status: str) -> list:
        return [
            incident for incident in self.incidents
            if incident["status"] == status
        ]