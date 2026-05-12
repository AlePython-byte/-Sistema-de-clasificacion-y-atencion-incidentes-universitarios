from app.utils.ui_stub import ui

from app.pages.dashboard_page import DashboardPage
from app.pages.incident_page import IncidentPage
from app.pages.queue_page import QueuePage
from app.pages.report_page import ReportPage


def create_app():
    ui.title('CampusCare - Frontend')

    dashboard = DashboardPage()
    incident = IncidentPage()
    queue = QueuePage()
    report = ReportPage()

    @ui.page('/')
    def index():
        return dashboard.render()

    @ui.page('/incidents')
    def incidents():
        return incident.render()

    @ui.page('/queue')
    def queue_page():
        return queue.render()

    @ui.page('/reports')
    def reports():
        return report.render()


if __name__ == '__main__':
    create_app()
    ui.run()
