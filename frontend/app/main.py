import streamlit as st
from app.pages import dashboard_page, incidents_page, queue_page

# Configuración inicial de la página
st.set_page_config(
    page_title="CampusCare - Sistema de Incidentes",
    page_icon="🎓",
    layout="wide"
)

def main():
    # Barra lateral de navegación
    st.sidebar.title("CampusCare")
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100) # Imagen genérica de campus/educación
    
    st.sidebar.write("### Navegación")
    
    # Menú de navegación
    opciones = {
        "📊 Panel de Control": dashboard_page.show,
        "📋 Gestión de Incidentes": incidents_page.show,
        "🚦 Atención y Registro": queue_page.show
    }
    
    seleccion = st.sidebar.radio("Ir a:", list(opciones.keys()))
    
    # Separador en la barra lateral
    st.sidebar.divider()
    st.sidebar.info(
        "**CampusCare v1.0**\n\n"
        "Sistema académico para registrar, consultar y gestionar incidentes universitarios."
    )
    
    # Mostrar la página seleccionada
    pagina_seleccionada = opciones[seleccion]
    pagina_seleccionada()

if __name__ == "__main__":
    main()
