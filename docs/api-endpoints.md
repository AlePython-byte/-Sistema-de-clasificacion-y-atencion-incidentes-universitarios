# Documentación de endpoints

Esta documentación resume los endpoints actuales del backend de CampusCare. Para probarlos visualmente, iniciar el servidor y abrir `http://127.0.0.1:8000/docs`.

## GET /

| Campo | Detalle |
|---|---|
| Método | `GET` |
| Ruta | `/` |
| Propósito | Verificar que la API esté respondiendo. |
| Body | No requiere. |
| Respuesta esperada | `{"message": "CampusCare API is running."}` |
| Posibles errores | No se esperan errores funcionales en uso normal. |

## GET /health

| Campo | Detalle |
|---|---|
| Método | `GET` |
| Ruta | `/health` |
| Propósito | Confirmar que el servicio está saludable. |
| Body | No requiere. |
| Respuesta esperada | `{"status": "healthy"}` |
| Posibles errores | No se esperan errores funcionales en uso normal. |

## POST /api/incidents/

| Campo | Detalle |
|---|---|
| Método | `POST` |
| Ruta | `/api/incidents/` |
| Propósito | Crear un nuevo incidente universitario. |
| Body | Requiere datos del incidente. |
| Respuesta esperada | Incidente creado con `id`, `priority`, `status`, `assigned_to` y `created_at`. |
| Posibles errores | `422 VALIDATION_ERROR` si el body no cumple las validaciones. |

Body esperado:

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

Respuesta esperada:

```json
{
  "id": "uuid-generado",
  "title": "Falla en proyector del aula 204",
  "description": "El proyector no enciende durante la clase de programación.",
  "category": "Tecnología",
  "location": "Bloque A - Aula 204",
  "reported_by": "Docente de programación",
  "urgency_level": "HIGH",
  "priority": "HIGH",
  "status": "OPEN",
  "assigned_to": null,
  "created_at": "2026-05-12T22:00:00.000000Z"
}
```

## GET /api/incidents/

| Campo | Detalle |
|---|---|
| Método | `GET` |
| Ruta | `/api/incidents/` |
| Propósito | Listar todos los incidentes guardados en memoria. |
| Body | No requiere. |
| Respuesta esperada | Lista de incidentes. |
| Posibles errores | No se esperan errores funcionales en uso normal. |

Respuesta esperada:

```json
[
  {
    "id": "uuid-generado",
    "title": "Falla en proyector del aula 204",
    "description": "El proyector no enciende durante la clase de programación.",
    "category": "Tecnología",
    "location": "Bloque A - Aula 204",
    "reported_by": "Docente de programación",
    "urgency_level": "HIGH",
    "priority": "HIGH",
    "status": "OPEN",
    "assigned_to": null,
    "created_at": "2026-05-12T22:00:00.000000Z"
  }
]
```

## GET /api/incidents/{incident_id}

| Campo | Detalle |
|---|---|
| Método | `GET` |
| Ruta | `/api/incidents/{incident_id}` |
| Propósito | Consultar un incidente por su ID. |
| Body | No requiere. |
| Respuesta esperada | Incidente encontrado. |
| Posibles errores | `404 HTTP_ERROR` si el incidente no existe. |

Ejemplo de error:

```json
{
  "detail": "Incident not found",
  "status_code": 404,
  "error": "HTTP_ERROR"
}
```

## PATCH /api/incidents/{incident_id}/status

| Campo | Detalle |
|---|---|
| Método | `PATCH` |
| Ruta | `/api/incidents/{incident_id}/status` |
| Propósito | Actualizar el estado de un incidente. |
| Body | Requiere el nuevo estado. |
| Respuesta esperada | Incidente actualizado. |
| Posibles errores | `404 HTTP_ERROR` si no existe, `422 VALIDATION_ERROR` si el estado no es válido. |

Body esperado:

```json
{
  "status": "IN_PROGRESS"
}
```

Estados permitidos:

- `OPEN`
- `ASSIGNED`
- `IN_PROGRESS`
- `RESOLVED`
- `CLOSED`

## PATCH /api/incidents/{incident_id}/assign

| Campo | Detalle |
|---|---|
| Método | `PATCH` |
| Ruta | `/api/incidents/{incident_id}/assign` |
| Propósito | Asignar un responsable a un incidente. |
| Body | Requiere `assigned_to`, aunque el schema permite `null` para mantener flexibilidad temporal. |
| Respuesta esperada | Incidente actualizado con responsable. |
| Posibles errores | `404 HTTP_ERROR` si no existe, `422 VALIDATION_ERROR` si el body no es válido. |

Body esperado:

```json
{
  "assigned_to": "Equipo de mantenimiento"
}
```

## GET /api/incidents/queue/next

| Campo | Detalle |
|---|---|
| Método | `GET` |
| Ruta | `/api/incidents/queue/next` |
| Propósito | Obtener el incidente abierto con mayor prioridad. |
| Body | No requiere. |
| Respuesta esperada | Incidente abierto con mayor prioridad, o `null` si no hay incidentes abiertos. |
| Posibles errores | No se esperan errores funcionales en uso normal. |

Nota importante: este endpoint ya usa `PriorityQueueManager`, pero todavía trabaja con datos en memoria.
