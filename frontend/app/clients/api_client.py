import requests
from typing import List, Dict


class ApiClient:
    def __init__(self, base_url: str = 'http://localhost:8000'):
        self.base_url = base_url.rstrip('/')

    def _get(self, path: str):
        try:
            resp = requests.get(f"{self.base_url}{path}", timeout=3)
            resp.raise_for_status()
            return resp.json()
        except Exception:
            return None

    def get_incidents(self) -> List[Dict]:
        data = self._get('/incidents')
        if data is None:
            # fallback simulated data
            return [
                {
                    'id': 1,
                    'title': 'Falla eléctrica en laboratorio',
                    'description': 'Corte de energía en sala 101',
                    'category': 'Infrastructure',
                    'location': 'Building A - Room 101',
                    'priority': 'High',
                    'status': 'Open'
                },
            ]
        return data

    def create_incident(self, data: Dict) -> Dict:
        try:
            resp = requests.post(f"{self.base_url}/incidents", json=data, timeout=3)
            resp.raise_for_status()
            return resp.json()
        except Exception:
            # return the posted data as a simulated created object
            simulated = data.copy()
            simulated.setdefault('id', 999)
            simulated.setdefault('priority', 'Normal')
            simulated.setdefault('status', 'Open')
            return simulated

    def get_next_incident(self) -> Dict:
        data = self._get('/incidents/next')
        if data is None:
            return {
                'id': 2,
                'title': 'Accidente menor en campus',
                'description': 'Persona con mareos cerca de biblioteca',
                'category': 'Health',
                'location': 'Library',
                'priority': 'Critical',
                'status': 'Pending'
            }
        return data

    def get_reports(self) -> Dict:
        data = self._get('/reports/summary')
        if data is None:
            return {
                'total_incidents': 42,
                'open': 10,
                'critical': 3,
                'resolved': 29
            }
        return data
