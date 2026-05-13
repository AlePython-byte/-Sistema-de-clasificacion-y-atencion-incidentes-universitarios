import requests
from typing import List, Dict, Optional, Any

BASE_URL = "http://127.0.0.1:8000/api"

class CampusCareAPI:
    """Cliente para comunicarse con el backend de CampusCare."""
    
    @staticmethod
    def get_incidents() -> List[Dict[str, Any]]:
        """Obtiene la lista de todos los incidentes."""
        try:
            response = requests.get(f"{BASE_URL}/incidents/")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error al obtener incidentes: {e}")
            return []
            
    @staticmethod
    def get_incident(incident_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene un incidente por su ID."""
        try:
            response = requests.get(f"{BASE_URL}/incidents/{incident_id}")
            if response.status_code == 404:
                return None
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error al obtener el incidente {incident_id}: {e}")
            return None

    @staticmethod
    def create_incident(data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Crea un nuevo incidente."""
        try:
            response = requests.post(f"{BASE_URL}/incidents/", json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error al crear incidente: {e}")
            return None

    @staticmethod
    def update_status(incident_id: str, new_status: str) -> Optional[Dict[str, Any]]:
        """Actualiza el estado de un incidente."""
        try:
            response = requests.patch(
                f"{BASE_URL}/incidents/{incident_id}/status", 
                json={"status": new_status}
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error al actualizar estado: {e}")
            return None

    @staticmethod
    def assign_responsible(incident_id: str, assigned_to: str) -> Optional[Dict[str, Any]]:
        """Asigna un responsable a un incidente."""
        try:
            response = requests.patch(
                f"{BASE_URL}/incidents/{incident_id}/assign", 
                json={"assigned_to": assigned_to}
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error al asignar responsable: {e}")
            return None

    @staticmethod
    def get_next_incident() -> Optional[Dict[str, Any]]:
        """Obtiene el siguiente incidente abierto."""
        try:
            response = requests.get(f"{BASE_URL}/incidents/queue/next")
            if response.status_code == 404:
                return None
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error al obtener el siguiente incidente: {e}")
            return None
