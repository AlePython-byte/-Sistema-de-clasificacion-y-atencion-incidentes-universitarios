# Visión general del backend

## Qué contiene el backend

El backend de CampusCare contiene una API REST inicial construida con FastAPI. Permite registrar incidentes universitarios, consultarlos, actualizar su estado, asignar responsables y obtener de forma temporal el siguiente incidente abierto.

Este bloque corresponde al Integrante 1. Su objetivo es dejar una base clara, funcional y mantenible para que otros integrantes puedan continuar sin tener que reorganizar el proyecto.

## División por carpetas

```text
backend/
+-- app/
|   +-- main.py
|   +-- api/
|   +-- core/
|   +-- schemas/
|   +-- services/
|   +-- repositories/
|   +-- tests/
+-- requirements.txt
```

## Responsabilidades de cada carpeta

| Carpeta o archivo | Responsabilidad |
|---|---|
| `app/main.py` | Crea la aplicación FastAPI, registra rutas y configura manejadores de errores. |
| `app/api/` | Contiene los endpoints expuestos por la API. |
| `app/core/` | Contiene configuración general del proyecto. |
| `app/schemas/` | Define modelos Pydantic para requests, responses, enums y errores. |
| `app/services/` | Contiene la lógica de aplicación simple. |
| `app/repositories/` | Contiene el almacenamiento temporal en memoria. |
| `app/tests/` | Contiene pruebas automatizadas básicas. |
| `requirements.txt` | Lista las dependencias necesarias para ejecutar y probar el backend. |

## Flujo de una petición

1. El cliente envía una petición HTTP a un endpoint, por ejemplo `POST /api/incidents/`.
2. FastAPI recibe la petición en `incident_routes.py`.
3. Pydantic valida el body usando los schemas de `incident_schema.py`.
4. La ruta llama a `IncidentService`.
5. El servicio aplica reglas simples, como estado inicial `OPEN` y prioridad basada en `urgency_level`.
6. El servicio usa `IncidentRepository` para guardar o consultar datos en memoria.
7. El resultado vuelve al servicio, luego a la ruta y finalmente al cliente como JSON.

## Manejo de errores

Los errores HTTP y de validación se centralizan en `main.py`. Esto evita que cada endpoint tenga que construir manualmente respuestas de error.

Formato general:

```json
{
  "detail": "Incident not found",
  "status_code": 404,
  "error": "HTTP_ERROR"
}
```

## Partes temporales

- `IncidentRepository` guarda datos en un diccionario en memoria.
- Los datos se pierden al reiniciar el servidor.
- `get_next_incident` devuelve el primer incidente abierto, no usa una cola de prioridad real.
- No hay autenticación, roles ni permisos.
- No hay base de datos.
- No hay frontend.

## Punto de integración futuro

El método `get_next_incident` en `IncidentService` contiene un TODO para integrar después `PriorityQueueManager`. Esa integración corresponde al bloque de estructuras avanzadas y no se implementa en este avance.
