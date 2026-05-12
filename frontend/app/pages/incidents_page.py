import streamlit as st
import pandas as pd
from app.clients.api_client import CampusCareAPI

def show():
    st.title("📋 Gestión de Incidentes")
    st.write("Listado y administración de todos los incidentes del sistema.")

    incidents = CampusCareAPI.get_incidents()

    if not incidents:
        st.info("No hay incidentes para mostrar.")
        return

    # Preparar datos para la tabla
    df = pd.DataFrame(incidents)
    # Seleccionar columnas importantes para la vista principal
    cols_to_show = ["id", "title", "category", "urgency_level", "status", "assigned_to", "created_at"]
    df_show = df[cols_to_show].copy()

    st.dataframe(df_show, use_container_width=True)

    st.divider()

    st.subheader("Acciones sobre un Incidente")
    
    # Selector de incidente
    incident_options = {inc["id"]: f"{inc['title']} ({inc['status']})" for inc in incidents}
    selected_id = st.selectbox("Selecciona un incidente para gestionar:", options=list(incident_options.keys()), format_func=lambda x: incident_options[x])

    if selected_id:
        # Obtener detalle del incidente seleccionado
        selected_inc = next((inc for inc in incidents if inc["id"] == selected_id), None)
        
        if selected_inc:
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Detalles:**")
                st.write(f"**ID:** {selected_inc['id']}")
                st.write(f"**Título:** {selected_inc['title']}")
                st.write(f"**Descripción:** {selected_inc['description']}")
                st.write(f"**Ubicación:** {selected_inc['location']}")
                st.write(f"**Reportado por:** {selected_inc['reported_by']}")
                
            with col2:
                st.write("**Gestión:**")
                st.write(f"**Categoría:** {selected_inc['category']}")
                st.write(f"**Urgencia / Prioridad:** {selected_inc['urgency_level']} / {selected_inc['priority']}")
                st.write(f"**Estado Actual:** {selected_inc['status']}")
                st.write(f"**Asignado a:** {selected_inc['assigned_to'] if selected_inc['assigned_to'] else 'Nadie'}")

            st.divider()
            
            st.write("### Actualizar")
            col_update_status, col_update_assign = st.columns(2)
            
            with col_update_status:
                new_status = st.selectbox(
                    "Cambiar Estado", 
                    options=["OPEN", "ASSIGNED", "IN_PROGRESS", "RESOLVED", "CLOSED"],
                    index=["OPEN", "ASSIGNED", "IN_PROGRESS", "RESOLVED", "CLOSED"].index(selected_inc['status']) if selected_inc['status'] in ["OPEN", "ASSIGNED", "IN_PROGRESS", "RESOLVED", "CLOSED"] else 0
                )
                if st.button("Actualizar Estado", key=f"btn_status_{selected_id}"):
                    res = CampusCareAPI.update_status(selected_id, new_status)
                    if res:
                        st.success(f"Estado actualizado a {new_status}")
                        st.rerun()
                    else:
                        st.error("Error al actualizar el estado.")
            
            with col_update_assign:
                new_assign = st.text_input("Asignar a (Nombre o Equipo)", value=selected_inc['assigned_to'] if selected_inc['assigned_to'] else "")
                if st.button("Asignar Responsable", key=f"btn_assign_{selected_id}"):
                    if new_assign.strip():
                        res = CampusCareAPI.assign_responsible(selected_id, new_assign)
                        if res:
                            st.success(f"Incidente asignado a {new_assign}")
                            st.rerun()
                        else:
                            st.error("Error al asignar responsable.")
                    else:
                        st.warning("El campo de responsable no puede estar vacío.")
