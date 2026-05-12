import streamlit as st
from app.clients.api_client import CampusCareAPI

def show():
    st.title("Atención y Registro")

    tab_atencion, tab_registro = st.tabs(["🚦 Siguiente a Atender", "📝 Registrar Incidente"])

    with tab_atencion:
        st.header("Siguiente Incidente en Cola")
        st.write("Obtén el incidente con mayor prioridad (o el primero abierto) que requiere atención.")

        if st.button("Obtener Siguiente Incidente"):
            next_inc = CampusCareAPI.get_next_incident()

            if next_inc:
                st.success("¡Incidente encontrado!")
                st.write("---")
                st.write(f"### {next_inc['title']}")
                st.write(f"**ID:** {next_inc['id']}")
                st.write(f"**Categoría:** {next_inc['category']} | **Ubicación:** {next_inc['location']}")
                st.write(f"**Prioridad:** {next_inc['priority']} | **Urgencia:** {next_inc['urgency_level']}")
                st.write(f"**Descripción:** {next_inc['description']}")
                st.write(f"**Reportado por:** {next_inc['reported_by']}")
                st.write("---")
                st.info("Para gestionar este incidente, ve a la pestaña de 'Gestión de Incidentes'.")
            else:
                st.info("No hay incidentes abiertos en este momento. ¡Buen trabajo!")

    with tab_registro:
        st.header("Registrar Nuevo Incidente")
        st.write("Completa el siguiente formulario para registrar un problema en el campus.")

        with st.form("form_registro_incidente"):
            titulo = st.text_input("Título del Incidente", max_chars=100, help="De 5 a 100 caracteres.")
            descripcion = st.text_area("Descripción Detallada", max_chars=500, help="De 10 a 500 caracteres.")
            
            col1, col2 = st.columns(2)
            with col1:
                categoria = st.selectbox("Categoría", ["Tecnología", "Infraestructura", "Seguridad", "Limpieza", "Otro"])
                urgencia = st.selectbox("Nivel de Urgencia", ["LOW", "MEDIUM", "HIGH", "CRITICAL"])
            with col2:
                ubicacion = st.text_input("Ubicación", help="Ej. Bloque A - Aula 204")
                reportado_por = st.text_input("Reportado Por", help="Nombre, correo o rol de quien reporta.")

            submit_button = st.form_submit_button("Registrar Incidente")

            if submit_button:
                if not titulo or not descripcion or not ubicacion or not reportado_por:
                    st.error("Por favor, completa todos los campos del formulario.")
                elif len(titulo) < 5:
                    st.error("El título debe tener al menos 5 caracteres.")
                elif len(descripcion) < 10:
                    st.error("La descripción debe tener al menos 10 caracteres.")
                else:
                    nuevo_incidente = {
                        "title": titulo.strip(),
                        "description": descripcion.strip(),
                        "category": categoria,
                        "location": ubicacion.strip(),
                        "reported_by": reportado_por.strip(),
                        "urgency_level": urgencia
                    }
                    
                    res = CampusCareAPI.create_incident(nuevo_incidente)
                    if res:
                        st.success(f"¡Incidente registrado exitosamente! ID: {res['id']}")
                    else:
                        st.error("Ocurrió un error al registrar el incidente. Revisa la consola o el backend.")
