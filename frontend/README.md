# CampusCare - Frontend

Este es el módulo de interfaz de usuario del proyecto **CampusCare**, desarrollado asumiendo el rol del **Integrante 4 (Frontend y Experiencia de Usuario)**. 

El objetivo principal de este componente es consumir la API REST del backend de CampusCare y proveer una interfaz visual amigable y completamente en español para que los usuarios puedan gestionar incidentes dentro del campus.

## Funcionalidades Principales

Se ha construido una aplicación interactiva que permite:

1. **Panel de Control (Dashboard):** Visualizar el estado general del sistema y estadísticas de los incidentes registrados.
2. **Gestión de Incidentes:** Listar todos los incidentes con la capacidad de:
   - Ver sus detalles en profundidad.
   - Cambiar su estado a lo largo de su ciclo de vida (`OPEN`, `ASSIGNED`, `IN_PROGRESS`, `RESOLVED`, `CLOSED`).
   - Asignar un responsable o equipo de atención.
3. **Atención a Incidentes:** Ver el "Siguiente incidente" más prioritario que se encuentra abierto en el sistema, obteniéndolo directamente de la cola de atención del backend.
4. **Registro:** Un formulario completo y validado para reportar un nuevo incidente (falla tecnológica, problema de infraestructura, etc.).

## Tecnologías Utilizadas

- **Python**: El lenguaje principal, manteniendo consistencia con el backend.
- **Streamlit**: Framework que permite crear aplicaciones web dinámicas y modernas para datos usando únicamente Python.
- **Requests**: Librería estándar para interactuar con los endpoints del backend HTTP.

## Estructura del Código

La estructura ha sido organizada para ser modular y escalable:

```text
frontend/
├── app/
│   ├── main.py                # Punto de entrada de la aplicación y barra de navegación lateral.
│   ├── clients/
│   │   └── api_client.py      # Clase CampusCareAPI que agrupa todas las llamadas HTTP al backend.
│   ├── pages/                 # Contiene la lógica visual de cada pantalla independiente.
│   │   ├── dashboard_page.py
│   │   ├── incidents_page.py
│   │   └── queue_page.py
│   └── components/
│       └── __init__.py        # Preparado para componentes visuales reutilizables.
└── requirements.txt           # Dependencias exactas para levantar el proyecto.
```

## Requisitos y Configuración

Antes de iniciar el frontend, **es imprescindible que el backend esté en ejecución**. Por defecto, este cliente intenta conectarse a `http://127.0.0.1:8000/api`.

### Pasos para ejecutar:

1. Abre una terminal de comandos (como PowerShell) y navega a la carpeta `frontend`:
   ```powershell
   cd frontend
   ```

2. (Opcional pero recomendado) Crea y activa un entorno virtual de Python para mantener las dependencias aisladas:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Instala las dependencias necesarias leyendo el archivo de requerimientos:
   ```powershell
   pip install -r requirements.txt
   ```

4. Ejecuta la aplicación de Streamlit:
   ```powershell
   streamlit run app/main.py
   ```

El servidor local de Streamlit arrancará y automáticamente abrirá una pestaña en tu navegador web predeterminado (por lo general en `http://localhost:8501`) mostrando la interfaz en español de CampusCare.
