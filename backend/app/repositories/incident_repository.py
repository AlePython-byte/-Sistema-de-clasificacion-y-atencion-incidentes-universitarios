import json
import os
from datetime import datetime

class IncidentRepository:
    def __init__(self, storage_path: str = "incidents.json") -> None:
        self.storage_path = storage_path
        self._incidents: dict[str, dict] = self._load_from_disk()

    def _load_from_disk(self) -> dict:
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r") as f:
                    data = json.load(f)
                    # Convert ISO strings back to datetime objects for Pydantic/logic
                    for inc in data.values():
                        if "created_at" in inc and isinstance(inc["created_at"], str):
                            try:
                                inc["created_at"] = datetime.fromisoformat(inc["created_at"])
                            except ValueError:
                                pass
                    return data
            except (json.JSONDecodeError, IOError):
                return {}
        return {}

    def _save_to_disk(self) -> None:
        try:
            # We need to serialize datetimes to strings for JSON
            serializable_data = {}
            for k, v in self._incidents.items():
                copy_v = v.copy()
                if isinstance(copy_v.get("created_at"), datetime):
                    copy_v["created_at"] = copy_v["created_at"].isoformat()
                serializable_data[k] = copy_v

            with open(self.storage_path, "w") as f:
                json.dump(serializable_data, f, indent=4)
        except IOError as e:
            print(f"Error saving to disk: {e}")

    def save(self, incident: dict) -> dict:
        self._incidents[incident["id"]] = incident
        self._save_to_disk()
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
        self._save_to_disk()
        return incident


