from dataclasses import dataclass
from typing import Dict


@dataclass
class IncidentViewModel:
    incident_id: int
    title: str
    description: str
    category: str
    location: str
    priority: str
    status: str

    def to_table_row(self) -> Dict:
        return {
            'ID': self.incident_id,
            'Título': self.title,
            'Descripción': self.description,
            'Categoría': self.category,
            'Ubicación': self.location,
            'Prioridad': self.priority,
            'Estado': self.status,
        }
