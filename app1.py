import streamlit as st
from streamlit_option_menu import option_menu
import sqlite3
from passlib.context import CryptContext

# Configuración de la base de datos
DB_NAME = "db/beyond_platform.db"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def get_user_by_email(conn, email: str):
    cur = conn.cursor()
    cur.execute("SELECT * FROM usuarios WHERE username = ?", (email,))
    return cur.fetchone()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

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
            "nav-link-selected": {"background-color": "#7c82ce"},
        }

    )

# Importar los dashboards
from dashboards.videos_dashboard import show as show_videos_dashboard
from dashboards.podcasts_dashboard import show as show_podcasts_dashboard
from dashboards.admin_dashboard import show as show_admin_dashboard
from dashboards.beyond_summit_dashboard import show as show_beyond_summit_dashboard 
from dashboards.init_dashboard import show as show_init_dashboard

# Reset admin login when navigating away from Admin Space
if selected != "Admin Space" and "admin_logged_in" in st.session_state:
    del st.session_state.admin_logged_in

# Mostrar el dashboard correspondiente según la opción seleccionada
if selected == "Inicio":
    show_init_dashboard()
elif selected == "Charlas":
    show_videos_dashboard()    
elif selected == "Podcasts":
    show_podcasts_dashboard()
elif selected == "Beyond Summit":
    show_beyond_summit_dashboard()
elif selected == "Admin Space":
    # Always require login for Admin Space
    if "admin_logged_in" not in st.session_state or not st.session_state.admin_logged_in:
        st.title("🔐 Admin Login")
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            with st.form("admin_login_form"):
                st.markdown("### Acceso Restringido")
                st.info("Solo administradores autorizados pueden acceder a esta sección.")
                
                email = st.text_input("Usuario/Email", placeholder="Ingresa tu usuario")
                password = st.text_input("Contraseña", type="password", placeholder="Ingresa tu contraseña")
                
                col1, col2, col3 = st.columns([1, 1, 1])
                with col2:
                    submitted = st.form_submit_button("🚀 Ingresar", use_container_width=True)
                
                if submitted:
                    if email and password:
                        conn = get_db()
                        user = get_user_by_email(conn, email)
                        conn.close()
                        
                        if user and user["rol"] == "admin" and verify_password(password, user["password"]):
                            st.session_state.admin_logged_in = True
                            st.success("✅ Login exitoso. Bienvenido al Admin Space.")
                            st.rerun()
                        else:
                            st.error("❌ Credenciales incorrectas o no tienes permisos de administrador.")
                    else:
                        st.warning("⚠️ Por favor completa todos los campos.")
    else:
        # Show logout button in sidebar when logged in
        with st.sidebar:
            st.markdown("---")
            st.success("✅ Sesión activa como Admin")
            if st.button("🚪 Cerrar Sesión"):
                del st.session_state.admin_logged_in
                st.rerun()
        
        show_admin_dashboard()

