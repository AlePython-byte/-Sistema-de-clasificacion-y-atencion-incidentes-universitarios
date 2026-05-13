# Reglas de negocio

Este documento describe la integración realizada por el Integrante 3 sobre el backend de CampusCare.

## Alcance del bloque

Se integraron estructuras de datos al flujo real del servicio de incidentes sin cambiar rutas, sin agregar frontend, sin base de datos real y sin autenticación.

## Reglas implementadas

- `get_next_incident` ahora usa una cola de prioridad real con `PriorityQueueManager`.
- Los incidentes con prioridad `CRITICAL` se atienden antes que `HIGH`, `MEDIUM` y `LOW`.
- Si dos incidentes tienen la misma prioridad, se conserva el orden de inserción entregado a la cola.
- Solo se consideran incidentes con estado `OPEN` para el siguiente incidente a atender.
- Asignar un responsable a un incidente `OPEN` cambia su estado a `ASSIGNED`.
- Un incidente `CLOSED` no puede volver a `OPEN`.
- Un incidente `CLOSED` no puede ser reasignado.
- Un incidente `RESOLVED` puede pasar a `CLOSED`.
- Si un incidente no existe, se mantiene la respuesta `404`.

## Uso de PriorityQueueManager

`PriorityQueueManager` se usa dentro de `IncidentService.get_next_incident`.

Flujo actual:

1. El servicio obtiene todos los incidentes desde el repositorio en memoria.
2. Filtra los incidentes con estado `OPEN`.
3. Agrega esos incidentes a `PriorityQueueManager`.
4. La cola devuelve el incidente con mayor prioridad.
5. El incidente se responde usando el mismo `IncidentResponse` existente.

Este proceso no elimina incidentes del repositorio. Solo calcula cuál debe atenderse primero.

## Uso de IncidentHistoryStack

`IncidentHistoryStack` se usa internamente en `IncidentService` para registrar eventos básicos.

Eventos registrados:

- `INCIDENT_CREATED`
- `INCIDENT_ASSIGNED`
- `STATUS_CHANGED`

Cada evento contiene:

- `incident_id`
- `action`
- `previous_value`
- `new_value`
- `created_at`

El historial todavía no tiene endpoint público. Puede consultarse internamente mediante `get_incident_history(incident_id)`.

## CategoryTree

`CategoryTree` ya existe y está probado, pero todavía no está conectado al flujo principal del servicio. Su integración puede usarse después para clasificar incidentes por categorías y subcategorías.

## Limitaciones actuales

- No hay base de datos real.
- El repositorio sigue siendo en memoria.
- Los datos se pierden al reiniciar el servidor.
- El historial vive en memoria dentro del servicio.
- No hay endpoint público para consultar historial.
- No hay autenticación ni roles.
- No hay frontend.

## Validación

Para validar este bloque:

```powershell
cd backend
python -m compileall app
python -m pytest
```

Las pruebas cubren prioridad, reglas de estado, asignación, errores 404 e historial interno.
