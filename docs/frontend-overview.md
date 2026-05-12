# CampusCare - Frontend

Este documento describe la arquitectura y el funcionamiento del frontend de **CampusCare**, implementado como parte de las responsabilidades del Integrante 4.

## Tecnologías Utilizadas
- **Python 3**
- **Streamlit**: Framework principal para construir la interfaz web.
- **Requests**: Librería para consumir la API REST del backend.
- **Pandas**: Utilizado internamente por Streamlit para renderizar tablas y datos de forma eficiente.

## Estructura de Directorios

```text
frontend/
├── app/
│   ├── main.py                 # Punto de entrada de la aplicación Streamlit y menú lateral.
│   ├── clients/
│   │   └── api_client.py       # Clase CampusCareAPI para centralizar las peticiones HTTP al backend.
│   ├── components/
│   │   └── __init__.py         # Paquete preparado para futuros componentes UI reutilizables.
│   └── pages/
│       ├── dashboard_page.py   # Pantalla "Panel de Control": métricas y resumen de incidentes.
│       ├── incidents_page.py   # Pantalla "Gestión de Incidentes": listado, cambio de estado y asignación.
│       └── queue_page.py       # Pantalla "Atención y Registro": obtener siguiente incidente en cola y formulario de creación.
└── requirements.txt            # Dependencias del proyecto (streamlit, requests).
```

## Flujo Visual del Usuario

1. **Navegación**: Al iniciar la aplicación, el usuario ve una barra lateral a la izquierda con tres opciones de menú principales.
2. **Panel de Control**: Vista rápida para entender el volumen de incidentes y su distribución por estado. Ideal para supervisores.
3. **Gestión de Incidentes**: 
   - Muestra una tabla con todos los incidentes.
   - Permite seleccionar un incidente específico usando un desplegable.
   - Al seleccionar uno, se muestran sus detalles (Ubicación, Reportado por, Descripción) y permite dos acciones clave:
     - Cambiar su estado (ej. de `OPEN` a `IN_PROGRESS`).
     - Asignar a un responsable o equipo.
4. **Atención y Registro**: Dividido en dos pestañas:
   - *Siguiente a Atender*: Un botón que llama al endpoint `/queue/next` del backend y muestra el incidente más urgente que necesita atención.
   - *Registrar Incidente*: Un formulario claro en español para que cualquier usuario pueda reportar un nuevo problema. Al enviarlo, se valida en frontend y luego se envía al backend.

## Cómo Ejecutar el Frontend Localmente

1. Asegúrate de tener el backend corriendo (ver instrucciones en el `README.md` principal). El backend debe estar expuesto en `http://127.0.0.1:8000`.
2. Abre una nueva terminal en Visual Studio Code.
3. Navega a la carpeta del proyecto y crea un entorno virtual para el frontend (opcional pero recomendado):
   ```powershell
   cd frontend
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
4. Ejecuta la aplicación de Streamlit:
   ```powershell
   streamlit run app/main.py
   ```
5. El navegador se abrirá automáticamente en la dirección local proporcionada por Streamlit (usualmente `http://localhost:8501`).
