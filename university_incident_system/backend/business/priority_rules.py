class PriorityRules:
    """
    Business rules responsible for calculating the priority of an incident.
    """

    def calculate_priority(self, category: str, description: str) -> str:
        clean_description = description.lower().strip()

        high_priority_keywords = [
            "herido",
            "accidente",
            "robo",
            "amenaza",
            "incendio",
            "emergencia",
            "pelea",
            "riesgo"
        ]

        medium_priority_keywords = [
            "daño",
            "falla",
            "sin internet",
            "eléctrico",
            "electrico",
            "bloqueado",
            "avería",
            "averia"
        ]

        for keyword in high_priority_keywords:
            if keyword in clean_description:
                return "Alta"

        for keyword in medium_priority_keywords:
            if keyword in clean_description:
                return "Media"

        if category in ["Seguridad", "Bienestar Universitario"]:
            return "Alta"

        if category in ["Tecnología", "Mantenimiento"]:
            return "Media"

        return "Baja"