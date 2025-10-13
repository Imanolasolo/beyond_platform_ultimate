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

col1, col2 = st.columns([1, 6])
with col1:
    st.image('assets/images/Beyond_logo.jpg', width=200)
with col2:
    selected = option_menu(
        menu_title=None,  # Sin título del menú
        options=["Inicio", "Charlas", "Podcasts", "Beyond Summit", "Iniciar sesión"],  # Opciones del menú
        # icons eliminado para quitar iconos
        menu_icon=" ",  # Sin icono de menú ni flecha
        default_index=0,  # Opción seleccionada por defecto
        orientation="horizontal",  # Menú horizontal
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            # "icon": {"color": "orange", "font-size": "20px"},
            "nav-link": {
                "font-size": "16px",
                "font-family": "monospace",
                "text-align": "left",
                "margin": "0px",
                "color": "black",
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

# Reset admin login when navigating away from Iniciar sesión
if selected != "Iniciar sesión" and "admin_logged_in" in st.session_state:
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
elif selected == "Iniciar sesión":
    # Always require login for Iniciar sesión
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





import base64

with open("assets/images/Beyond_logo.jpg", "rb") as f:
    logo_data = base64.b64encode(f.read()).decode()
with open("assets/images/muyu_logo_1.png", "rb") as f:
    muyu_logo_data = base64.b64encode(f.read()).decode()

footer_original = f"""
<style>
.footer-original {{
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100vw;
        background-color: #7c82ce;
        color: white;
        padding: 12px 0 8px 0;
        font-size: 16px;
        z-index: 9999;
}}
.footer-flex {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        max-width: 1200px;
        margin: 0 auto;
        width: 100%;
}}
.footer-logo {{
        flex: 0 0 auto;
        display: flex;
        align-items: center;
}}
.footer-center {{
        flex: 1 1 auto;
        text-align: center;
}}
.footer-linkedin {{
        flex: 0 0 auto;
        margin-left: 16px;
        display: flex;
        align-items: center;
}}
</style>
<div class="footer-original">
    <div class="footer-flex">
            <div class="footer-logo" style="display: flex; align-items: center;">
                <img src="data:image/png;base64,{logo_data}" alt="Beyond Logo" style="height:50px; vertical-align: middle; margin-right: 24px;">
            </div>
            <div style="display: flex; align-items: center; flex: 1 1 auto; justify-content: center;">
                <div style="width:2px; height:50px; background:white; margin-right:24px; margin-left:6px;"></div>
                                                <div style="color:white; font-size:16px; font-family:monospace; margin-right:24px; display:flex; flex-direction:column; align-items:center;">
                                                    <span>Beyond Platform es<br>parte de Muyu Education.</span>
                                                                                            <div style='display:flex; align-items:center; gap:10px; margin-top:4px;'>
                                                                                                <img src="data:image/png;base64,{muyu_logo_data}" alt="Muyu Logo" style="height:32px;"/>
                                                                                            </div>
                                                </div>
                <div style="width:2px; height:50px; background:white; margin-left:6px; margin-right:24px;"></div>
                                <div style="color:white; font-size:16px; font-family:monospace; text-align:center; display:flex; align-items:center; justify-content:center; gap:8px;">
                                    <span>Sigue a Beyond</span>
                                    <a href="https://www.linkedin.com/in/tu-perfil-linkedin" target="_blank" title="LinkedIn" style="color: white; text-decoration: none; display:inline-flex; align-items:center;">
                                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="20" height="20"><path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-10h3v10zm-1.5-11.268c-.966 0-1.75-.784-1.75-1.75s.784-1.75 1.75-1.75 1.75.784 1.75 1.75-.784 1.75-1.75 1.75zm15.5 11.268h-3v-5.604c0-1.337-.025-3.063-1.868-3.063-1.868 0-2.154 1.459-2.154 2.968v5.699h-3v-10h2.881v1.367h.041c.401-.761 1.379-1.563 2.838-1.563 3.036 0 3.6 2.001 3.6 4.601v5.595z"/></svg>
                                    </a>
                                    <span style="margin-left:12px;">&copy; 2024 Beyond Platform - Todos los derechos reservados.</span>
                                </div>
            </div>
    </div>
</div>
"""
st.markdown(footer_original, unsafe_allow_html=True)