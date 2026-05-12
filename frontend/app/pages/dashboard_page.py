import streamlit as st
from app.clients.api_client import CampusCareAPI

def show():
    st.title("📊 Panel de Control (Dashboard)")
    st.write("Resumen del estado actual de los incidentes en CampusCare.")

    incidents = CampusCareAPI.get_incidents()

    if not incidents:
        st.info("No hay incidentes registrados actualmente.")
        return

    total = len(incidents)
    
    # Contadores por estado
    estados = {"OPEN": 0, "ASSIGNED": 0, "IN_PROGRESS": 0, "RESOLVED": 0, "CLOSED": 0}
    for inc in incidents:
        est = inc.get("status", "OPEN")
        if est in estados:
            estados[est] += 1

    # Métricas principales
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Incidentes", total)
    col2.metric("Abiertos (OPEN)", estados["OPEN"])
    col3.metric("En Progreso (IN_PROGRESS)", estados["IN_PROGRESS"])

    st.divider()

    col4, col5, col6 = st.columns(3)
    col4.metric("Asignados (ASSIGNED)", estados["ASSIGNED"])
    col5.metric("Resueltos (RESOLVED)", estados["RESOLVED"])
    col6.metric("Cerrados (CLOSED)", estados["CLOSED"])

    st.divider()
    
    # Gráfico simple (barras)
    st.subheader("Distribución por Estado")
    data = {
        "Estado": list(estados.keys()),
        "Cantidad": list(estados.values())
    }
    st.bar_chart(data, x="Estado", y="Cantidad")
