import heapq
from typing import Any, Dict, List, Tuple
from app.schemas.incident_schema import IncidentPriority

class PriorityQueueManager:
    """
    Manages incidents using a priority queue.
    Critical incidents are handled first.
    """
    def __init__(self):
        self._queue: List[Tuple[int, int, Dict[str, Any]]] = []
        self._counter = 0  # To handle tie-breakers when priorities are equal
        
        self._priority_map = {
            IncidentPriority.CRITICAL: 1,
            IncidentPriority.HIGH: 2,
            IncidentPriority.MEDIUM: 3,
            IncidentPriority.LOW: 4
        }
        
    def enqueue(self, incident: Dict[str, Any]):
        priority_enum = incident.get('priority', IncidentPriority.LOW)
        if isinstance(priority_enum, str):
            try:
                priority_enum = IncidentPriority(priority_enum.upper())
            except ValueError:
                priority_enum = IncidentPriority.LOW

        priority_score = self._priority_map.get(priority_enum, 4)
        
        heapq.heappush(self._queue, (priority_score, self._counter, incident))
        self._counter += 1
        
    def dequeue(self) -> Dict[str, Any] | None:
        if self.is_empty():
            return None
        return heapq.heappop(self._queue)[2]
        
    def peek(self) -> Dict[str, Any] | None:
        if self.is_empty():
            return None
        return self._queue[0][2]
        
    def is_empty(self) -> bool:
        return len(self._queue) == 0
        
    def size(self) -> int:
        return len(self._queue)
