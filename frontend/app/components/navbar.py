from nicegui import ui


class Navbar:
    def __init__(self):
        pass

    def render(self):
        with ui.row().classes('items-center gap-6'):
            ui.link('Inicio', '/').props('underline=false')
            ui.link('Incidentes', '/incidents').props('underline=false')
            ui.link('Cola de atención', '/queue').props('underline=false')
            ui.link('Reportes', '/reports').props('underline=false')
