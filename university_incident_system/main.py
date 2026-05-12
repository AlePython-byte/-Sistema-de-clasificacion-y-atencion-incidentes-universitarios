from backend.services.incident_service import IncidentService
from backend.services.report_service import ReportService


def show_incident(incident: dict) -> None:
    print("----------------------------------------")
    print(f"ID: {incident['id']}")
    print(f"Título: {incident['title']}")
    print(f"Descripción: {incident['description']}")
    print(f"Ubicación: {incident['location']}")
    print(f"Reportado por: {incident['reporter_name']}")
    print(f"Categoría: {incident['category']}")
    print(f"Prioridad: {incident['priority']}")
    print(f"Departamento asignado: {incident['assigned_department']}")
    print(f"Estado: {incident['status']}")


def show_report(title: str, report: dict) -> None:
    print(f"\n{title}")
    print("----------------------------------------")

    for key, value in report.items():
        print(f"{key}: {value}")


def main() -> None:
    incident_service = IncidentService()
    report_service = ReportService()

    incident_service.create_incident(
        title="Falla de internet",
        description="No hay internet en el laboratorio de sistemas",
        location="Bloque B - Sala 203",
        reporter_name="Carlos Martínez"
    )

    incident_service.create_incident(
        title="Problema de seguridad",
        description="Se reporta una amenaza cerca de la entrada principal",
        location="Entrada principal",
        reporter_name="Laura Gómez"
    )

    incident_service.create_incident(
        title="Salón sucio",
        description="El salón tiene basura acumulada desde la mañana",
        location="Bloque A - Aula 101",
        reporter_name="Andrés Pérez"
    )

    incident_service.create_incident(
        title="Falla eléctrica",
        description="Hay un daño eléctrico en el aula de audiovisuales",
        location="Bloque C - Aula 305",
        reporter_name="María Rodríguez"
    )

    incident_service.update_status(1, "En proceso")
    incident_service.update_status(2, "Pendiente")
    incident_service.update_status(3, "Resuelto")
    incident_service.update_status(4, "En proceso")

    print("\nSISTEMA DE CLASIFICACIÓN Y ATENCIÓN DE INCIDENTES UNIVERSITARIOS")
    print("===============================================================")

    print("\nINCIDENTES REGISTRADOS")
    for incident in incident_service.get_all_incidents():
        show_incident(incident)

    summary_report = report_service.generate_summary_report(
        incident_service.get_all_incidents()
    )

    department_report = report_service.generate_department_report(
        incident_service.get_all_incidents()
    )

    category_report = report_service.generate_category_report(
        incident_service.get_all_incidents()
    )

    show_report("REPORTE GENERAL", summary_report)
    show_report("REPORTE POR DEPARTAMENTO", department_report)
    show_report("REPORTE POR CATEGORÍA", category_report)


if __name__ == "__main__":
    main()