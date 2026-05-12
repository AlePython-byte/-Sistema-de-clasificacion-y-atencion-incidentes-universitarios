# CampusCare

## Descripción del proyecto

CampusCare es un sistema académico para registrar, consultar, asignar y priorizar incidentes universitarios. Su propósito es servir como base para gestionar reportes dentro del campus, como fallas tecnológicas, problemas de infraestructura o situaciones que requieran atención prioritaria.

## Objetivo del sistema

El sistema busca organizar los reportes de incidentes para que puedan ser atendidos de forma más clara y ordenada. En esta etapa inicial, el backend permite crear incidentes, consultarlos, cambiar su estado, asignar un responsable y obtener temporalmente el siguiente incidente abierto.

## Alcance actual

Este avance corresponde al Integrante 1: Backend/API Developer.

Incluye:

- Backend base con FastAPI.
- Endpoints principales de incidentes.
- Validaciones con Pydantic.
- Manejo consistente de errores.
- Repositorio temporal en memoria.
- Pruebas básicas con pytest.
- Documentación Swagger automática.

## Lo que NO incluye todavía

Este bloque todavía no incluye:
- Base de datos real.
- Autenticación.
- Roles de usuario.
- Estructuras avanzadas.
- Cola de prioridad real.
- Reportes avanzados.
- Persistencia después de reiniciar el servidor.

## Tecnologías utilizadas

- Python.
- FastAPI.
- Pydantic.
- Uvicorn.
- Pytest.
- HTTPX.

## Estructura del proyecto

```text
campuscare/
+-- backend/
|   +-- app/
|   |   +-- main.py
|   |   +-- api/
|   |   |   +-- __init__.py
|   |   |   +-- incident_routes.py
|   |   +-- core/
|   |   |   +-- __init__.py
|   |   |   +-- config.py
|   |   +-- schemas/
|   |   |   +-- __init__.py
|   |   |   +-- incident_schema.py
|   |   |   +-- error_schema.py
|   |   +-- services/
|   |   |   +-- __init__.py
|   |   |   +-- incident_service.py
|   |   +-- repositories/
|   |   |   +-- __init__.py
|   |   |   +-- incident_repository.py
|   |   +-- tests/
|   |       +-- __init__.py
|   |       +-- test_health.py
|   |       +-- test_incident_routes.py
|   +-- requirements.txt
|   +-- docs/
|   +-- handoff-notes.md
+-- frontend/
|   +-- app/
|   |   +-- main.py
|   |   +-- clients/
|   |   |   +-- api_client.py
|   |   +-- pages/
|   |   |   +-- dashboard_page.py
|   |   |   +-- incidents_page.py
|   |   |   +-- queue_page.py
|   |   +-- components/
|   |       +-- __init__.py
|   +-- requirements.txt
+-- docs/
|   +-- backend-overview.md
|   +-- api-endpoints.md
|   +-- frontend-overview.md
|   +-- handoff-notes.md
|   +-- integration-plan.md
|   +-- team-handoff.md
|   +-- git-workflow.md
|   +-- data-structures.md
|   +-- business-rules.md
+-- README.md
+-- .gitignore
```

## Instalación y ejecución en Visual Studio Code

Abrir una terminal de Windows PowerShell en Visual Studio Code y ejecutar:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Si `uvicorn` no se reconoce por el PATH de Windows, usar:

```powershell
python -m uvicorn app.main:app --reload
```

## Ejecución del Frontend

Una vez que el backend esté corriendo, abre una nueva terminal y ejecuta:

```powershell
cd frontend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app/main.py
```

Esto abrirá la aplicación web en tu navegador, lista para usar en español.

## Acceso a Swagger

Con el servidor encendido, abrir:

```text
http://127.0.0.1:8000/docs
```

Swagger permite probar los endpoints desde el navegador y ver las validaciones generadas por Pydantic.

## Endpoints disponibles

| Método HTTP | Ruta | Descripción | Estado actual |
|---|---|---|---|
| GET | `/` | Verifica que la API esté funcionando. | Funcional |
| GET | `/health` | Devuelve el estado saludable del servicio. | Funcional |
| POST | `/api/incidents/` | Crea un nuevo incidente. | Funcional |
| GET | `/api/incidents/` | Lista todos los incidentes registrados en memoria. | Funcional |
| GET | `/api/incidents/{incident_id}` | Busca un incidente por ID. | Funcional |
| PATCH | `/api/incidents/{incident_id}/status` | Actualiza el estado de un incidente. | Funcional |
| PATCH | `/api/incidents/{incident_id}/assign` | Asigna un responsable a un incidente. | Funcional |
| GET | `/api/incidents/queue/next` | Devuelve el incidente abierto con mayor prioridad. | Funcional en memoria |

## Ejemplo de creación de incidente

Body para `POST /api/incidents/`:

```json
{
  "title": "Falla en proyector del aula 204",
  "description": "El proyector no enciende durante la clase de programación.",
  "category": "Tecnología",
  "location": "Bloque A - Aula 204",
  "reported_by": "Docente de programación",
  "urgency_level": "HIGH"
}
```

## Validaciones principales

| Campo | Validación |
|---|---|
| `title` | Obligatorio, de 5 a 100 caracteres. |
| `description` | Obligatorio, de 10 a 500 caracteres. |
| `category` | Obligatorio, máximo 80 caracteres. |
| `location` | Obligatorio, máximo 120 caracteres. |
| `reported_by` | Obligatorio, máximo 100 caracteres. |
| `urgency_level` | Solo permite `LOW`, `MEDIUM`, `HIGH` o `CRITICAL`. |
| `status` | Solo permite `OPEN`, `ASSIGNED`, `IN_PROGRESS`, `RESOLVED` o `CLOSED`. |
| `assigned_to` | Opcional, máximo 100 caracteres. |

## Manejo de errores

Los errores HTTP y de validación usan un formato consistente para facilitar la integración con otros módulos.

Ejemplo para recurso no encontrado:

```json
{
  "detail": "Incident not found",
  "status_code": 404,
  "error": "HTTP_ERROR"
}
```

Ejemplo para error de validación:

```json
{
  "detail": "Validation error",
  "status_code": 422,
  "error": "VALIDATION_ERROR"
}
```

## Ejecución de pruebas

Con el entorno virtual activado:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python -m pytest
```

Actualmente pasan las pruebas básicas del backend. La última validación ejecutada en este bloque fue:

```text
36 passed
```

## Guía rápida para nuevos integrantes

Antes de continuar el proyecto, revisar estos documentos:

- `docs/integration-plan.md`: plan para integrar ramas, validar cambios y proteger la estabilidad de `main`.
- `docs/team-handoff.md`: resumen operativo para cambio de integrante o cambio de grupo.
- `docs/git-workflow.md`: flujo recomendado de Git para trabajar por ramas y resolver merges.
- `docs/data-structures.md`: explicación de las estructuras creadas por el Integrante 2.
- `docs/business-rules.md`: reglas de negocio e integración de estructuras del Integrante 3.

Validación mínima antes de entregar o mezclar cambios:

```powershell
cd backend
python -m compileall app
python -m pytest
```

## Decisiones técnicas del Integrante 1

- Se usa FastAPI por su claridad para construir APIs REST y por su documentación automática con Swagger.
- Se usa Pydantic para validar datos de entrada y salida.
- Se usa un repositorio en memoria porque la persistencia real será responsabilidad de otro bloque futuro.
- Se usa una arquitectura por capas para separar rutas, schemas, servicios y repositorios.
- `get_next_incident` usa `PriorityQueueManager`, pero todavía trabaja con el repositorio en memoria.

## Recomendaciones para los siguientes integrantes

### Para Integrante 2

- Mantener y extender estructuras de datos avanzadas si aparecen nuevas reglas.
- Revisar `PriorityQueueManager` si cambian los criterios de prioridad.
- Revisar `HistoryStack` si se decide exponer historial públicamente.
- Implementar `CategoryTree`.

### Para Integrante 3

- Mejorar reglas de negocio.
- Crear asignación avanzada.
- Crear reportes.
- Preparar persistencia real si aplica.

### Para Integrante 4

- Crear frontend en Python.
- Consumir endpoints del backend.
- Crear pantallas en español.
- Documentar flujo visual del usuario.

## Estado actual del backend

El backend está en estado funcional inicial y listo para continuar. Las rutas principales existen, las validaciones están activas, los errores tienen formato uniforme y las pruebas básicas pasan. Este bloque deja cerrado el alcance principal del Integrante 1.

La información se guarda en memoria, por lo tanto los incidentes creados se pierden al reiniciar el servidor.
