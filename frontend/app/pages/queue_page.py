from app.utils.ui_stub import ui

from app.components.page_header import PageHeader
from app.clients.api_client import ApiClient
from app.services.incident_frontend_service import IncidentFrontendService


class QueuePage:
    def __init__(self):
        api = ApiClient()
        self.service = IncidentFrontendService(api)

    def render(self):
        from app.components.navbar import Navbar
        Navbar().render()

        PageHeader('Cola de atención', 'Siguiente incidente por prioridad')

        incident = self.service.load_next_incident()

        with ui.card():
            ui.label(f"Título: {incident.title}")
            ui.label(f"Descripción: {incident.description}")
            ui.label(f"Ubicación: {incident.location}")
            ui.label(f"Prioridad: {incident.priority}")

        def refresh():
            ui.notify('Cola actualizada', color='blue')

        ui.button('Actualizar cola', on_click=refresh)
