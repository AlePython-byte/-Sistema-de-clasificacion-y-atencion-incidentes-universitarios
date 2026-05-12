from typing import Any, Dict, List

class IncidentHistoryStack:
    """
    Saves the history of changes using a Stack (LIFO).
    """
    def __init__(self):
        self._stack: List[Dict[str, Any]] = []
        
    def push(self, change_record: Dict[str, Any]):
        """
        Pushes a new change record onto the stack.
        """
        self._stack.append(change_record)
        
    def pop(self) -> Dict[str, Any] | None:
        """
        Removes and returns the most recent change record.
        """
        if self.is_empty():
            return None
        return self._stack.pop()
        
    def peek(self) -> Dict[str, Any] | None:
        """
        Returns the most recent change record without removing it.
        """
        if self.is_empty():
            return None
        return self._stack[-1]
        
    def is_empty(self) -> bool:
        return len(self._stack) == 0
        
    def size(self) -> int:
        return len(self._stack)
