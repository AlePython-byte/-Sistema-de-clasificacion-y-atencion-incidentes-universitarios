class PriorityQueueManager:
    def __init__(self):
        self.queue = []

    def add(self, item):
        self.queue.append(item)

    def get_next(self):
        if not self.queue:
            return None
        # Priority order: CRITICAL > HIGH > MEDIUM > LOW
        priority_map = {"CRITICAL": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1}
        # Assuming item is dict for now
        self.queue.sort(key=lambda x: priority_map.get(x.get("priority", "LOW"), 0), reverse=True)
        return self.queue.pop(0)
