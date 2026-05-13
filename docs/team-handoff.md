# Entrega rápida para integrantes o grupos

Este documento está pensado para cambios rápidos de grupo o integrante. Resume cómo arrancar el backend, qué está listo y qué limitaciones hay.

## Resumen rápido del proyecto

CampusCare es un sistema académico para gestionar incidentes universitarios. El backend actual permite registrar incidentes, listarlos, consultarlos por ID, actualizar su estado, asignar responsable y consultar el siguiente incidente abierto según prioridad.

## Cómo ejecutar el backend

Desde Visual Studio Code, abrir una terminal PowerShell:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Si `uvicorn` no se reconoce:

```powershell
python -m uvicorn app.main:app --reload
```

## Cómo probar Swagger

Con el servidor ejecutándose, abrir:

```text
http://127.0.0.1:8000/docs
```

Desde Swagger se pueden crear incidentes, listarlos, consultarlos por ID, actualizar estado, asignar responsable y probar el endpoint temporal de cola.

## Cómo correr pruebas

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python -m compileall app
python -m pytest
```

## Estado actual del backend

- Backend funcional con FastAPI.
- Swagger disponible.
- Validaciones activas con Pydantic.
- Errores HTTP y de validación con formato consistente.
- Repositorio en memoria.
- Pruebas automatizadas existentes.
- Documentación principal en español.

## Limitaciones actuales

- No hay frontend.
- No hay base de datos real.
- No hay autenticación.
- No hay roles de usuario.
- No hay estructuras avanzadas.
- La cola de prioridad ya existe, pero funciona sobre datos en memoria.
- No hay reportes avanzados.
- No hay persistencia al reiniciar el servidor.

## Qué debe hacer cada nuevo integrante

### Integrante 1

- Mantener estable la rama principal.
- Revisar merges.
- Ejecutar pruebas antes de aceptar cambios.
- Mantener documentación en español.
- Proteger el contrato actual de la API.

### Integrante 2

- Mantener y extender estructuras de datos avanzadas si aparecen nuevas reglas.
- Revisar `PriorityQueueManager` si cambian los criterios de prioridad.
- Revisar historial con `HistoryStack` si se decide exponerlo públicamente.
- Implementar clasificación por categorías con `CategoryTree` si aplica.
- No cambiar rutas públicas sin coordinar con Integrante 1.

### Integrante 3

- Mejorar reglas de negocio.
- Diseñar asignación avanzada.
- Preparar reportes.
- Coordinar cualquier cambio de persistencia o modelo de datos.
- Mantener compatibilidad con los schemas existentes cuando sea posible.

### Integrante 4

- Crear frontend en Python.
- Consumir los endpoints existentes.
- Crear pantallas en español.
- Documentar el flujo visual del usuario.
- No modificar backend salvo coordinación explícita.

## Advertencias importantes

El repositorio actual es en memoria. Los incidentes creados se pierden al reiniciar el servidor.

El endpoint `/api/incidents/queue/next` usa `PriorityQueueManager`. Sigue siendo una implementación en memoria y debe revisarse si luego se agrega base de datos o persistencia real.

## Antes de entregar el turno

- Guardar cambios.
- Revisar `git status`.
- Ejecutar pruebas si se modificó backend.
- Actualizar documentación si cambió algún flujo.
- Avisar limitaciones o conflictos pendientes al siguiente grupo.
