import streamlit as st
from streamlit_option_menu import option_menu

# Configurar la página
st.set_page_config(
    page_title="Beyond Summit",
    page_icon=":guardsman:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Crear una barra de navegación superior CON LOGO
col1,col2 = st.columns ([1,6])
with col1:
    st.image('assets/images/Beyond_logo.jpg', width=200)
with col2:    
    selected = option_menu(
        menu_title='Beyond, your growing partner',
        options=["Inicio", "Charlas", "Podcasts","Beyond Summit","Admin Space"],  # Opciones del menú
        icons=["house", "info-circle", "envelope"],  # Iconos para las opciones
        menu_icon="cast",  # Icono del menú
        default_index=0,  # Opción seleccionada por defecto
        orientation="horizontal",  # Menú horizontal
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "orange", "font-size": "20px"}, 
            "nav-link": {
                "font-size": "16px",
                "font-family": "Roboto, 'Times New Roman', serif",
                "text-align": "left",
                "margin":"0px",
                "--hover-color": "#eee",
            },
            "nav-link-selected": {"background-color": "#c52f37"},
        }

    )

# Importar los dashboards
from dashboards.videos_dashboard import show as show_videos_dashboard
from dashboards.podcasts_dashboard import show as show_podcasts_dashboard
from dashboards.admin_dashboard import show as show_admin_dashboard
from dashboards.beyond_summit_dashboard import show as show_beyond_summit_dashboard 

# Mostrar el dashboard correspondiente según la opción seleccionada
if selected == "Inicio":
    st.title("Bienvenido a Beyond Platform")
    st.write("Explora nuestras charlas y podcasts para inspirarte y aprender.") 
elif selected == "Charlas":
    show_videos_dashboard()    
elif selected == "Podcasts":
    show_podcasts_dashboard()
elif selected == "Beyond Summit":
    show_beyond_summit_dashboard()
elif selected == "Admin Space":
    show_admin_dashboard()

