from app.utils.ui_stub import ui

from app.components.page_header import PageHeader
from app.components.stat_card import StatCard
from app.clients.api_client import ApiClient
from app.services.incident_frontend_service import IncidentFrontendService


class DashboardPage:
    def __init__(self):
        api = ApiClient()
        self.service = IncidentFrontendService(api)

    def render(self):
        navbar = ui.row()
        from app.components.navbar import Navbar
        Navbar().render()

        PageHeader('Panel principal', 'Resumen rápido de incidentes')

        summary = self.service.load_report_summary()

        with ui.row().classes('gap-4'):
            StatCard('Total de incidentes', str(summary.get('total_incidents', '-')),'Cantidad total de incidentes registrados').render()
            StatCard('Incidentes abiertos', str(summary.get('open', '-')),'Incidentes en estado abierto').render()
            StatCard('Incidentes críticos', str(summary.get('critical', '-')),'Incidentes con prioridad crítica').render()
            StatCard('Incidentes resueltos', str(summary.get('resolved', '-')),'Incidentes ya resueltos').render()
