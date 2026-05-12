class AssignmentService:
    """
    Service responsible for assigning incidents to university departments.
    """

    def assign_department(self, category: str) -> str:
        departments = {
            "Tecnología": "Departamento de Soporte Técnico",
            "Mantenimiento": "Área de Mantenimiento",
            "Seguridad": "Departamento de Seguridad Universitaria",
            "Servicios Generales": "Área de Servicios Generales",
            "Bienestar Universitario": "Bienestar Universitario",
            "General": "Mesa de Ayuda"
        }

        return departments.get(category, "Mesa de Ayuda")