# Estructuras de datos

Este documento describe las estructuras implementadas por el Integrante 2 para CampusCare. Las estructuras están aisladas del servicio principal para no romper el contrato actual de la API.

## Estado actual

Las estructuras ya existen y tienen pruebas unitarias. `PriorityQueueManager` e `IncidentHistoryStack` ya están integradas en `IncidentService`; `CategoryTree` sigue lista para una integración futura.

La integración debe mantenerse coordinada para evitar cambios de comportamiento no controlados.

## Archivos creados

| Archivo | Estructura |
|---|---|
| `backend/app/structures/priority_queue.py` | `PriorityQueueManager` |
| `backend/app/structures/history_stack.py` | `IncidentHistoryStack` |
| `backend/app/structures/category_tree.py` | `CategoryTree` |
| `backend/app/tests/test_structures.py` | Pruebas unitarias de estructuras |

## PriorityQueueManager

`PriorityQueueManager` administra incidentes usando una cola de prioridad basada en `heapq`.

Sirve para obtener primero los incidentes más urgentes. El orden de prioridad es:

1. `CRITICAL`
2. `HIGH`
3. `MEDIUM`
4. `LOW`

Reglas importantes:

- Los incidentes se representan como `dict`.
- Si falta el campo `priority`, se usa `LOW` como valor por defecto.
- Si dos incidentes tienen la misma prioridad, sale primero el que fue agregado primero.
- Usa un contador interno para resolver empates.
- Ya se usa indirectamente desde el endpoint `/api/incidents/queue/next` a través de `IncidentService`.

Métodos principales:

- `add_incident(incident: dict) -> None`
- `get_next_incident() -> dict | None`
- `peek_next_incident() -> dict | None`
- `is_empty() -> bool`
- `size() -> int`
- `clear() -> None`

## IncidentHistoryStack

`IncidentHistoryStack` administra eventos de historial usando una pila basada en `list`.

Sirve para registrar eventos y recuperar primero el último evento agregado. Esto puede ser útil para historial de cambios de estado, auditoría simple o seguimiento de acciones sobre incidentes.

Reglas importantes:

- Los eventos se representan como `dict`.
- `pop_event` devuelve el último evento agregado y lo elimina.
- `peek_event` devuelve el último evento sin eliminarlo.
- `get_events` devuelve una copia para evitar modificar la pila interna desde afuera.

Métodos principales:

- `push_event(event: dict) -> None`
- `pop_event() -> dict | None`
- `peek_event() -> dict | None`
- `get_events() -> list[dict]`
- `is_empty() -> bool`
- `size() -> int`
- `clear() -> None`

## CategoryTree

`CategoryTree` administra categorías y subcategorías en forma jerárquica.

Sirve para representar grupos como:

```text
Tecnología
  Internet
  Proyector
Infraestructura
  Electricidad
  Mobiliario
Seguridad
  Acceso
  Emergencia
```

Reglas importantes:

- Si `parent_name` es `None`, la categoría se agrega como raíz.
- Si `parent_name` existe, la categoría se agrega como hija.
- Si `parent_name` no existe, se lanza `ValueError`.
- No se permiten nombres vacíos.
- No se duplican categorías con el mismo nombre.
- `get_tree` devuelve una representación completa de la jerarquía.

Métodos principales:

- `add_category(name: str, parent_name: str | None = None) -> None`
- `find_category(name: str) -> dict | None`
- `get_tree() -> dict`
- `get_children(name: str) -> list[str]`
- `category_exists(name: str) -> bool`
- `clear() -> None`

## Pruebas

Las pruebas están en:

```text
backend/app/tests/test_structures.py
```

Cubren:

- Orden de prioridad.
- Orden de inserción cuando hay empate.
- Operaciones básicas de cola, pila y árbol.
- Casos vacíos.
- Limpieza con `clear`.
- Validación de padre inexistente en categorías.
- Prevención de duplicados.

## Próximo paso para integración

El Integrante 3 ya conectó `PriorityQueueManager` y `IncidentHistoryStack` al flujo del servicio principal.

Queda pendiente:

- Usar `CategoryTree` para clasificar incidentes por categorías y subcategorías.
- Mantener las rutas actuales para no romper el frontend ni Swagger.
