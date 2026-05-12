from typing import Any, List, Optional


class IncidentHistoryStack:
    """
    Manages a history of changes using a stack (LIFO).
    """

    def __init__(self):
        self._stack: List[Any] = []

    def push(self, change: Any) -> None:
        """
        Adds a change record to the top of the stack.
        """
        self._stack.append(change)

    def pop(self) -> Optional[Any]:
        """
        Removes and returns the most recent change.
        """
        if self.is_empty():
            return None
        return self._stack.pop()

    def peek(self) -> Optional[Any]:
        """
        Returns the most recent change without removing it.
        """
        if self.is_empty():
            return None
        return self._stack[-1]

    def is_empty(self) -> bool:
        """
        Returns True if the stack is empty.
        """
        return len(self._stack) == 0

    def size(self) -> int:
        """
        Returns the number of records in the history.
        """
        return len(self._stack)

    def clear(self) -> None:
        """
        Clears all history.
        """
        self._stack.clear()
