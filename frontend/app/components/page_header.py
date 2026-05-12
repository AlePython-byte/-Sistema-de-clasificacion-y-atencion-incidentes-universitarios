from app.utils.ui_stub import ui


class PageHeader:
    def __init__(self, title: str, subtitle: str = ''):
        self.title = title
        self.subtitle = subtitle

    def render(self):
        with ui.column().classes('gap-0'):
            ui.h1(self.title)
            if self.subtitle:
                ui.label(self.subtitle).classes('text-sm text-gray-600')
