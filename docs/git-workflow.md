# Flujo de trabajo con Git

Este documento define un flujo simple para evitar conflictos y proteger la estabilidad del proyecto CampusCare.

## Reglas principales

- No trabajar directamente en `main`.
- Crear ramas por funcionalidad o tarea.
- Hacer commits pequeños y descriptivos.
- Actualizar `main` antes de mezclar.
- Revisar cambios con `git diff --name-status`.
- Hacer merge de una rama a la vez.
- Correr pruebas después de cada merge.
- No hacer push si hay conflictos.
- Usar `git status` frecuentemente.
- Si un merge sale mal, abortarlo con `git merge --abort`.

## Crear una rama de trabajo

```powershell
git checkout main
git pull origin main
git checkout -b feature/nombre-de-la-tarea
```

Ejemplos de nombres:

- `feature/integration-cleanup`
- `feature/priority-queue`
- `feature/business-rules`
- `feature/frontend-ui`

## Revisar cambios antes de integrar una rama

```powershell
git checkout main
git pull origin main
git fetch origin
git diff --name-status main..origin/nombre-rama
```

Este comando ayuda a ver qué archivos serán afectados antes de hacer merge.

## Mezclar una rama

```powershell
git checkout main
git pull origin main
git fetch origin
git merge origin/nombre-rama
```

Después del merge:

```powershell
cd backend
python -m compileall app
python -m pytest
```

## Revisar estado del repositorio

```powershell
git status
```

Usar este comando antes y después de cada merge.

## Si aparece un conflicto

No hacer push.

Revisar estado:

```powershell
git status
```

Abrir los archivos en conflicto y resolverlos manualmente. Cuidar especialmente:

- Rutas de API.
- Schemas.
- Tests.
- README.
- Documentos de `docs/`.

Si el conflicto no se puede resolver con seguridad:

```powershell
git merge --abort
```

Luego coordinar con el equipo.

## Antes de hacer push

Verificar:

- No hay conflictos.
- Las pruebas pasan.
- No se borraron archivos importantes.
- La documentación está actualizada.
- El código sigue en inglés.
- La documentación sigue en español.

Comandos recomendados:

```powershell
git status
git diff --name-status
cd backend
python -m compileall app
python -m pytest
```

## Criterio de merge seguro

Una rama puede integrarse cuando:

- Tiene un objetivo claro.
- No mezcla tareas de varios integrantes sin coordinación.
- Mantiene rutas existentes.
- Incluye pruebas si agrega comportamiento nuevo.
- No rompe Swagger.
- Pasa las validaciones locales.
