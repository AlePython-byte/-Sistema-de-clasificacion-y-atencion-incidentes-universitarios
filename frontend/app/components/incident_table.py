from nicegui import ui
from typing import List


class IncidentTable:
    def __init__(self, incidents: List[dict]):
        self.incidents = incidents

    def render(self):
        # prepare rows from incidents (expecting dicts returned by IncidentViewModel.to_table_row)
        rows = [list(i.values()) for i in self.incidents]
        # column headers in Spanish
        columns = ['ID', 'Título', 'Descripción', 'Categoría', 'Ubicación', 'Prioridad', 'Estado']
        ui.table(columns, rows)
