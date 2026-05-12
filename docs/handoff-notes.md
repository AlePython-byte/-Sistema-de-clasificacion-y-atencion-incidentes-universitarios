# Notas de entrega para cambio de grupo

Este documento resume el estado del backend para que otro grupo pueda continuar rápidamente durante el intercambio por horas.

## Qué ya está hecho

- Backend base creado con FastAPI.
- Rutas principales de incidentes disponibles.
- Schemas Pydantic para creación, actualización de estado, asignación y respuesta.
- Enums simples para urgencia, estado y prioridad.
- Manejo consistente de errores HTTP y de validación.
- Repositorio temporal en memoria.
- Servicio de incidentes separado de las rutas.
- Pruebas básicas con pytest.
- Documentación Swagger automática.
- README principal en español.
- Documentación adicional en `docs/`.

## Qué se probó

Se validó:

- Compilación de archivos Python.
- Pruebas automatizadas del health check.
- Creación de incidentes.
- Listado de incidentes.
- Consulta por ID existente.
- Consulta por ID inexistente con error 404.
- Actualización de estado.
- Asignación de responsable.
- Validación de payload inválido con error 422.
- Endpoint temporal para siguiente incidente abierto.
- Endpoint temporal para siguiente incidente cuando no hay incidentes abiertos.

## Comandos usados

Desde la raíz del proyecto:

```powershell
python -m compileall backend
```

Desde `backend/`:

```powershell
python -m pytest
```

Para ejecutar el servidor:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

Si `uvicorn` no aparece en el PATH:

```powershell
python -m uvicorn app.main:app --reload
```

## Qué no se debe tocar sin coordinación

- No cambiar rutas existentes sin avisar al grupo, porque otros integrantes pueden depender de esos endpoints.
- No cambiar nombres de campos de request o response sin coordinar.
- No eliminar `IncidentResponse`, `IncidentCreateRequest`, `IncidentUpdateStatusRequest` ni `IncidentAssignRequest`.
- No reemplazar el repositorio en memoria por base de datos sin que el grupo lo acuerde.
- No implementar estructuras avanzadas dentro del bloque del Integrante 1.
- No mezclar frontend dentro de la carpeta del backend.

## Qué puede continuar el siguiente grupo

- Integrar una cola de prioridad real en `get_next_incident`.
- Agregar historial de cambios de estado.
- Agregar estructuras avanzadas según el rol del Integrante 2.
- Mejorar reglas de asignación y reportes según el rol del Integrante 3.
- Crear frontend que consuma estos endpoints según el rol del Integrante 4.
- Preparar persistencia real si el equipo decide agregar base de datos en un bloque posterior.

## Riesgos o limitaciones actuales

- Los datos no persisten después de reiniciar el servidor.
- El repositorio en memoria no es adecuado para producción.
- No hay autenticación ni roles.
- No hay control de permisos.
- No hay paginación ni filtros avanzados.
- La prioridad todavía es igual al nivel de urgencia.
- El endpoint `/api/incidents/queue/next` no usa una cola de prioridad real.

## Estado del repositorio en memoria

Los incidentes se guardan en un diccionario interno dentro de `IncidentRepository`. Esto permite probar el flujo completo desde Swagger o pytest sin instalar una base de datos.

Advertencia: cada vez que se reinicia el servidor, el diccionario se limpia y los incidentes creados se pierden.

## Estado final para entrega

El backend queda funcional en estado inicial, documentado en español y listo para que otro integrante o grupo continúe sin depender de explicaciones externas. Este bloque cierra el alcance principal del Integrante 1.
