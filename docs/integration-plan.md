# Plan de integración

Este documento define cómo integrar cambios en CampusCare sin romper la base del backend construida por el Integrante 1.

## Estado actual de main

La base actual del backend está funcional y lista para integración. Incluye una API REST con FastAPI, validaciones con Pydantic, manejo consistente de errores, repositorio temporal en memoria, pruebas automatizadas y documentación en español.

La rama `main` debe considerarse estable. Las ramas nuevas deben integrarse solo después de validar que no rompen el contrato actual de la API.

## Partes listas

- Estructura base del backend.
- Endpoints principales de incidentes.
- Schemas de request y response.
- ErrorResponse para errores consistentes.
- Repositorio en memoria.
- Servicio de incidentes con reglas simples.
- Swagger/OpenAPI configurado.
- Pruebas básicas con pytest.
- Documentación principal y documentación de apoyo en `docs/`.

## Partes faltantes

- Frontend.
- Base de datos real.
- Autenticación y roles.
- Cola de prioridad real.
- Estructuras avanzadas.
- Reglas de negocio más completas.
- Reportes avanzados.
- Persistencia después de reiniciar el servidor.

## Orden recomendado para integrar ramas

1. Integrar primero cambios de limpieza o documentación.
2. Integrar después cambios de estructuras internas que no modifiquen rutas.
3. Integrar cambios de reglas de negocio solo si mantienen los schemas actuales o documentan claramente los cambios.
4. Integrar persistencia real únicamente cuando el equipo acuerde el contrato de datos.
5. Integrar frontend al final o en paralelo, pero sin modificar el backend sin coordinación.

## Reglas antes de hacer merge

- No trabajar directamente en `main`.
- Revisar qué archivos cambia la rama.
- Confirmar que no se eliminaron tests ni schemas.
- Confirmar que no se cambiaron rutas existentes sin aprobación.
- Ejecutar validaciones locales.
- Revisar Swagger si se modificaron schemas o endpoints.
- Resolver conflictos antes de hacer push.

## Comandos para validar el proyecto

Antes de aceptar una rama, ejecutar:

```powershell
cd backend
python -m compileall app
python -m pytest
```

Si ambos comandos pasan, la rama puede pasar a revisión funcional.

## Archivos que no se deben borrar

- `backend/app/main.py`
- `backend/app/api/incident_routes.py`
- `backend/app/schemas/incident_schema.py`
- `backend/app/schemas/error_schema.py`
- `backend/app/services/incident_service.py`
- `backend/app/repositories/incident_repository.py`
- `backend/app/tests/test_health.py`
- `backend/app/tests/test_incident_routes.py`
- `README.md`
- `docs/backend-overview.md`
- `docs/api-endpoints.md`
- `docs/handoff-notes.md`
- `docs/integration-plan.md`
- `docs/team-handoff.md`
- `docs/git-workflow.md`

## Qué hacer si aparece un conflicto

1. No hacer push con conflictos.
2. Ejecutar `git status` para identificar archivos afectados.
3. Abrir cada archivo en conflicto y conservar la versión correcta combinando ambos cambios.
4. Evitar borrar rutas, schemas o pruebas existentes.
5. Después de resolver, ejecutar las validaciones.
6. Si el conflicto es grande o afecta contratos de API, coordinar con el equipo antes de continuar.

## Criterios para aceptar una rama

- Mantiene el backend ejecutable.
- No rompe rutas existentes.
- No elimina pruebas.
- No elimina documentación importante.
- Incluye pruebas nuevas si agrega comportamiento nuevo.
- Mantiene código en inglés y documentación en español.
- Pasa `python -m compileall app`.
- Pasa `python -m pytest`.
- Documenta cualquier cambio que afecte integración.

## Nota para el Integrante 1

El Integrante 1 debe actuar como guardián de estabilidad de `main`: revisar contratos, validar pruebas, proteger documentación y asegurar que los demás integrantes puedan continuar sin perder contexto.
