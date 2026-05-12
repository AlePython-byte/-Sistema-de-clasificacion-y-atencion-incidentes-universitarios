import heapq
from itertools import count


class PriorityQueueManager:
    _PRIORITY_ORDER = {
        "CRITICAL": 0,
        "HIGH": 1,
        "MEDIUM": 2,
        "LOW": 3,
    }

    def __init__(self) -> None:
        self._heap: list[tuple[int, int, dict]] = []
        self._counter = count()

    def add_incident(self, incident: dict) -> None:
        priority = self._get_priority_value(incident)
        insertion_order = next(self._counter)
        heapq.heappush(self._heap, (priority, insertion_order, incident))

    def get_next_incident(self) -> dict | None:
        if self.is_empty():
            return None

        return heapq.heappop(self._heap)[2]

    def peek_next_incident(self) -> dict | None:
        if self.is_empty():
            return None

        return self._heap[0][2]

    def is_empty(self) -> bool:
        return len(self._heap) == 0

    def size(self) -> int:
        return len(self._heap)

    def clear(self) -> None:
        self._heap.clear()
        self._counter = count()

    def _get_priority_value(self, incident: dict) -> int:
        priority = str(incident.get("priority", "LOW")).upper()
        return self._PRIORITY_ORDER.get(priority, self._PRIORITY_ORDER["LOW"])
