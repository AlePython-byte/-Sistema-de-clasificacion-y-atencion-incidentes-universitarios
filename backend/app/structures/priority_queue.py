import heapq
from typing import Any, List, Optional, Tuple


class PriorityQueueManager:
    """
    Manages incidents based on their priority level.
    Uses a min-heap where:
    0: CRITICAL
    1: HIGH
    2: MEDIUM
    3: LOW
    """

    PRIORITY_MAP = {
        "CRITICAL": 0,
        "HIGH": 1,
        "MEDIUM": 2,
        "LOW": 3
    }

    def __init__(self):
        self._queue: List[Tuple[int, Any]] = []

    def push(self, incident: Any, priority: str) -> None:
        """
        Adds an incident to the queue with the given priority.
        """
        priority_val = self.PRIORITY_MAP.get(priority.upper(), 3)
        heapq.heappush(self._queue, (priority_val, incident))

    def pop(self) -> Optional[Any]:
        """
        Removes and returns the incident with the highest priority (lowest value).
        """
        if not self._queue:
            return None
        return heapq.heappop(self._queue)[1]

    def peek(self) -> Optional[Any]:
        """
        Returns the incident with the highest priority without removing it.
        """
        if not self._queue:
            return None
        return self._queue[0][1]

    def is_empty(self) -> bool:
        """
        Returns True if the queue is empty.
        """
        return len(self._queue) == 0

    def size(self) -> int:
        """
        Returns the number of items in the queue.
        """
        return len(self._queue)
