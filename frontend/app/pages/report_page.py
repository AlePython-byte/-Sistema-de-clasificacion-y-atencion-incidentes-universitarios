from nicegui import ui

from app.components.page_header import PageHeader
from app.clients.api_client import ApiClient
from app.services.incident_frontend_service import IncidentFrontendService


class ReportPage:
    def __init__(self):
        api = ApiClient()
        self.service = IncidentFrontendService(api)

    def render(self):
        from app.components.navbar import Navbar
        Navbar().render()

        PageHeader('Reportes', 'Estadísticas básicas de incidentes')

        summary = self.service.load_report_summary()

        with ui.row().classes('gap-4'):
            ui.card().add(ui.label(f"Total de incidentes: {summary.get('total_incidents', '-') }"))
            ui.card().add(ui.label(f"Abiertos: {summary.get('open', '-') }"))
            ui.card().add(ui.label(f"Críticos: {summary.get('critical', '-') }"))
            ui.card().add(ui.label(f"Resueltos: {summary.get('resolved', '-') }"))
