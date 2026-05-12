from app.utils.ui_stub import ui

from app.components.page_header import PageHeader
from app.components.incident_table import IncidentTable
from app.clients.api_client import ApiClient
from app.services.incident_frontend_service import IncidentFrontendService


class IncidentPage:
    def __init__(self):
        api = ApiClient()
        self.service = IncidentFrontendService(api)

    def render(self):
        from app.components.navbar import Navbar
        Navbar().render()

        PageHeader('Incidentes', 'Registra y revisa incidentes')

        with ui.column().classes('w-full'):
            title = ui.input('Título')
            description = ui.textarea('Descripción')
            category = ui.input('Categoría')
            location = ui.input('Ubicación')
            def submit():
                self.service.register_incident(title.value, description.value, category.value, location.value)
                ui.notify('Incidente registrado', color='green')

            ui.button('Registrar incidente', on_click=submit)

        # load and show incidents
        incidents = self.service.load_incidents()
        rows = [i.to_table_row() for i in incidents]
        IncidentTable(rows).render()
