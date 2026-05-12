class ClassificationService:
    """
    Service responsible for classifying university incidents.
    """

    def classify_incident(self, description: str) -> str:
        clean_description = description.lower().strip()

        if self._contains_any(clean_description, ["internet", "wifi", "red", "computador", "sistema"]):
            return "Tecnología"

        if self._contains_any(clean_description, ["luz", "eléctrico", "electrico", "corriente", "bombillo", "cable"]):
            return "Mantenimiento"

        if self._contains_any(clean_description, ["robo", "pelea", "amenaza", "violencia", "seguridad"]):
            return "Seguridad"

        if self._contains_any(clean_description, ["basura", "sucio", "limpieza", "baño", "desorden"]):
            return "Servicios Generales"

        if self._contains_any(clean_description, ["accidente", "herido", "salud", "enfermo", "emergencia médica"]):
            return "Bienestar Universitario"

        return "General"

    def _contains_any(self, text: str, keywords: list[str]) -> bool:
        for keyword in keywords:
            if keyword in text:
                return True

        return False