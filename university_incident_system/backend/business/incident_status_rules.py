class IncidentStatusRules:
    """
    Business rules responsible for validating incident status changes.
    """

    VALID_STATUSES = [
        "Pendiente",
        "En proceso",
        "Resuelto",
        "Cancelado"
    ]

    def is_valid_status(self, status: str) -> bool:
        return status in self.VALID_STATUSES

    def can_change_status(self, current_status: str, new_status: str) -> bool:
        if not self.is_valid_status(new_status):
            return False

        if current_status == "Resuelto" and new_status == "Pendiente":
            return False

        if current_status == "Cancelado" and new_status != "Cancelado":
            return False

        return True