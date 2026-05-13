class IncidentHistoryStack:
    def __init__(self) -> None:
        self._events: list[dict] = []

    def push_event(self, event: dict) -> None:
        self._events.append(event)

    def pop_event(self) -> dict | None:
        if self.is_empty():
            return None

        return self._events.pop()

    def peek_event(self) -> dict | None:
        if self.is_empty():
            return None

        return self._events[-1]

    def get_events(self) -> list[dict]:
        return self._events.copy()

    def is_empty(self) -> bool:
        return len(self._events) == 0

    def size(self) -> int:
        return len(self._events)

    def clear(self) -> None:
        self._events.clear()
