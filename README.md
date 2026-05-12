# Frontend - CampusCare

## Sistema de Gestión y Priorización de Incidentes Universitarios

Este módulo corresponde al **frontend** del proyecto académico **CampusCare**, un sistema orientado a la gestión, clasificación, priorización y atención de incidentes dentro de un entorno universitario.

El frontend fue desarrollado completamente en **Python**, utilizando **NiceGUI** como herramienta principal para construir una interfaz web sencilla, clara y funcional. La aplicación permite que el usuario interactúe con el sistema mediante pantallas visuales en español, mientras que internamente el código mantiene una estructura organizada en inglés, siguiendo buenas prácticas de programación orientada a objetos.

---

## Objetivo del frontend

El objetivo principal de este módulo es ofrecer una interfaz gráfica que permita a los usuarios del sistema realizar acciones como:

- Consultar el panel principal del sistema.
- Registrar nuevos incidentes universitarios.
- Visualizar la lista de incidentes registrados.
- Consultar la cola de atención según prioridad.
- Revisar reportes básicos del sistema.
- Interactuar con el backend mediante una capa de cliente API.

Este frontend está diseñado para conectarse con un backend desarrollado en **FastAPI**, el cual se encarga de manejar la lógica de negocio, las estructuras de datos, la persistencia y los endpoints del sistema.

---

## Tecnologías utilizadas

| Tecnología | Uso dentro del proyecto |
|---|---|
| Python | Lenguaje principal del frontend |
| NiceGUI | Creación de la interfaz web |
| Requests | Consumo de endpoints del backend |
| Python Dotenv | Manejo opcional de variables de entorno |

---

## Estructura del módulo

```text
frontend/
├── app/
│   ├── main.py
│   │
│   ├── clients/
│   │   └── api_client.py
│   │
│   ├── components/
│   │   ├── navbar.py
│   │   ├── page_header.py
│   │   ├── incident_table.py
│   │   └── stat_card.py
│   │
│   ├── models/
│   │   └── incident_view_model.py
│   │
│   ├── pages/
│   │   ├── dashboard_page.py
│   │   ├── incident_page.py
│   │   ├── queue_page.py
│   │   └── report_page.py
│   │
│   └── services/
│       └── incident_frontend_service.py
│
├── requirements.txt
└── README.md
- The repository is currently in memory and can later be replaced by a database implementation.
- `get_next_incident` currently returns the first open incident found.
- A TODO is included in the service to integrate the future `PriorityQueueManager` from Integrante 2.
- The service and repository layers are separated so additional business rules can be added without changing the API routes directly.
- Other team members can add advanced prioritization, persistence, authentication, and frontend integration in their own blocks without changing the current API contract unnecessarily.
