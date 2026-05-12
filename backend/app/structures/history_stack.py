from datetime import datetime, timezone

class IncidentHistoryStack:
    def __init__(self):
        self.history = {}

    def push(self, incident_id: str, old_state: str, new_state: str, change_type: str = "status"):
        if incident_id not in self.history:
            self.history[incident_id] = []
        self.history[incident_id].append({
            "change_type": change_type,
            "old_state": old_state,
            "new_state": new_state,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
