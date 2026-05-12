class ReportService:
    """
    Service responsible for generating incident reports.
    """

    def generate_summary_report(self, incidents: list) -> dict:
        return {
            "total_incidents": len(incidents),
            "pending_incidents": self._count_by_field(incidents, "status", "Pendiente"),
            "in_process_incidents": self._count_by_field(incidents, "status", "En proceso"),
            "resolved_incidents": self._count_by_field(incidents, "status", "Resuelto"),
            "cancelled_incidents": self._count_by_field(incidents, "status", "Cancelado"),
            "high_priority_incidents": self._count_by_field(incidents, "priority", "Alta"),
            "medium_priority_incidents": self._count_by_field(incidents, "priority", "Media"),
            "low_priority_incidents": self._count_by_field(incidents, "priority", "Baja")
        }

    def generate_department_report(self, incidents: list) -> dict:
        report = {}

        for incident in incidents:
            department = incident["assigned_department"]

            if department not in report:
                report[department] = 0

            report[department] += 1

        return report

    def generate_category_report(self, incidents: list) -> dict:
        report = {}

        for incident in incidents:
            category = incident["category"]

            if category not in report:
                report[category] = 0

            report[category] += 1

        return report

    def _count_by_field(self, incidents: list, field: str, value: str) -> int:
        count = 0

        for incident in incidents:
            if incident[field] == value:
                count += 1

        return count