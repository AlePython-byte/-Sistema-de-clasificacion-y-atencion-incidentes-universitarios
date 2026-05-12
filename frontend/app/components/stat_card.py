from nicegui import ui


class StatCard:
    def __init__(self, title: str, value: str, description: str = ''):
        self.title = title
        self.value = value
        self.description = description

    def render(self):
        with ui.card().style('padding: 12px;'):
            ui.label(self.title).classes('text-sm text-gray-500')
            ui.h3(self.value).classes('text-2xl')
            if self.description:
                ui.label(self.description).classes('text-xs text-gray-600')
