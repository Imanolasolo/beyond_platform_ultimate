import streamlit as st
import sqlite3
from passlib.context import CryptContext
import base64

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
    # bcrypt solo admite hasta 72 bytes, truncar si es necesario
    return pwd_context.verify(plain_password[:72], hashed_password)

# Configurar la página
st.set_page_config(
    page_title="Beyond Summit",
    page_icon=":guardsman:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inyectar Roboto Condensed y estilos generales
st.markdown('''
    <link href="https://fonts.googleapis.com/css2?family=Roboto+Condensed:wght@400;700&display=swap" rel="stylesheet">
    <style>
    .roboto-expanded * {
        font-family: 'Roboto Condensed', Arial, sans-serif !important;
        letter-spacing: 0.04em;
    }
    </style>
''', unsafe_allow_html=True)

# Definición del menú (etiqueta visible, slug para query param)
menu_items = [
    ("**¿QUÉ ES BEYOND PLATFORM?**", "init"),
    ("**CHARLAS**", "charlas"),
    ("**PODCASTS**", "podcasts"),
    ("**BEYOND SUMMIT**", "summit"),
    ("**INICIAR SESIÓN**", "login"),
]
label_to_slug = {label: slug for label, slug in menu_items}
slug_to_label = {slug: label for label, slug in menu_items}
menu_options = [label for label, _ in menu_items]

# Leer query params y sincronizar con session_state
params = st.query_params or {}

menu_param_raw = params.get("menu")
if isinstance(menu_param_raw, list):
    menu_slug = menu_param_raw[0] if menu_param_raw else None
else:
    menu_slug = menu_param_raw

# Usar menu_slug como fuente de verdad; mantener selected_menu (label) por compatibilidad
if menu_slug and menu_slug in slug_to_label:
    st.session_state['menu_slug'] = menu_slug
    st.session_state['selected_menu'] = slug_to_label[menu_slug]
elif 'selected_menu' not in st.session_state or 'menu_slug' not in st.session_state:
    st.session_state['menu_slug'] = 'init'
    st.session_state['selected_menu'] = slug_to_label['init']

# NOTE: Debug expander removed to hide internal query params and session_state from UI.

# Cabecera en barra gris full-width que contiene logo y menú
current_menu = st.session_state.selected_menu

# Helper: sincroniza query params y session_state
def set_menu_slug(slug: str):
    if slug in slug_to_label:
        st.session_state['menu_slug'] = slug
        st.session_state['selected_menu'] = slug_to_label[slug]
    else:
        st.session_state['menu_slug'] = 'init'
        st.session_state['selected_menu'] = slug_to_label['init']
    # actualizar query params (uso de st.query_params)
    st.query_params = {"menu": [slug]}

# Helper: logout (limpia sólo flags/admin user y redirige a init)
def logout_admin():
    st.session_state.pop("admin_logged_in", None)
    st.session_state.pop("admin_user", None)
    set_menu_slug("init")

# Prepara el logo en base64 para embederlo en el header
try:
        with open("assets/images/beyond1.png", "rb") as _f:
                header_logo = base64.b64encode(_f.read()).decode()
except Exception:
        header_logo = ""

# Construir HTML de links con onclick para recarga limpia solo con ?menu=slug
menu_links_html = ""
for label, slug in menu_items:
    selected_class = "selected" if current_menu == label else ""
    link_text = label.replace("**", "")
    # onclick fuerza una recarga limpia solo con ?menu=slug (sin _ts ni otros params)
    menu_links_html += (
        f'<a href="?menu={slug}" '
        f'onclick="window.location.search=\'?menu={slug}\'; return false;" '
        f'class="custom-menu-link {selected_class}">{link_text}</a>'
    )

st.markdown(f'''
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Condensed:wght@400;700&display=swap');
    .top-bar {{
        position: relative;
        left: 0;
        right: 0;
        width: 100vw; /* ensure full viewport width */
        background: #f3f4f6; /* gris claro */
        padding: 10px 0;
        box-sizing: border-box;
        z-index: 9998;
    }}
    .top-bar-inner {{
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 16px;
        padding: 0 8px; /* reduce inner padding to remove left whitespace */
        box-sizing: border-box;
    }}
    .top-logo img {{ height:56px; }}
    .top-logo {{ margin-right: 380px; display:flex; align-items:center; }}
    /* menu stretches across available space; items centered in their area */
    /* menu stretches across available space; items aligned to the left next to logo */
    .custom-menu-row {{ display:flex; gap:18px; align-items:center; justify-content:flex-start; flex:1 1 auto; }}
    .custom-menu-link {{
        font-family: 'Roboto Condensed', Arial, sans-serif !important;
        font-size: 14px;
        color: #222 !important;
    text-decoration: none !important;
        padding: 8px 12px;
        border-bottom: 0px solid transparent;
        font-weight: 700;
        letter-spacing: 0.04em;
        transition: color .15s, background .15s, border-bottom .15s;
        display:inline-block;
    }}
    .custom-menu-link.selected {{ color: #7B2FF2 !important; border-bottom: 2px solid #7B2FF2 !important; }}
    .custom-menu-link:visited, .custom-menu-link:focus, .custom-menu-link:hover {{ text-decoration: none !important; }}
    .custom-menu-link, .custom-menu-link * {{ text-decoration: none !important; -webkit-text-decoration-skip-ink: none; text-decoration-skip-ink: none; }}
    .custom-menu-link:hover {{ background:#7B2FF2; color:#fff !important; border-bottom: 2px solid #7B2FF2; }}
    /* make the top bar span full width by removing Streamlit padding */
    .stApp > .css-1d391kg {{ padding-top: 0 !important; }}
</style>
<div class="top-bar">
    <div class="top-bar-inner">
        <div class="top-logo">
            <img src="data:image/png;base64,{header_logo}" alt="Beyond logo" />
        </div>
        <div class="custom-menu-row">
            {menu_links_html}
        </div>
    </div>
</div>
''', unsafe_allow_html=True)

selected = st.session_state.selected_menu

# Importar dashboards
from dashboards.videos_dashboard import show as show_videos_dashboard
from dashboards.podcasts_dashboard import show as show_podcasts_dashboard
from dashboards.admin_dashboard import show as show_admin_dashboard
from dashboards.beyond_summit_dashboard import show as show_beyond_summit_dashboard
from dashboards.init_dashboard import show as show_init_dashboard

# Mostrar el dashboard correspondiente según la opción seleccionada
if selected == "**¿QUÉ ES BEYOND PLATFORM?**":
    show_init_dashboard()
elif selected == "**CHARLAS**":
    show_videos_dashboard()
elif selected == "**PODCASTS**":
    show_podcasts_dashboard()
elif selected == "**BEYOND SUMMIT**":
    show_beyond_summit_dashboard()
elif selected == "**INICIAR SESIÓN**":
    # Login admin
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
                            # login: marcar sesión admin y usuario, redirigir a admin
                            st.session_state.admin_logged_in = True
                            st.session_state.admin_user = email
                            set_menu_slug("login")
                            st.success("✅ Login exitoso. Bienvenido al Admin Space.")
                            st.rerun()
                        else:
                            st.error("❌ Credenciales incorrectas o no tienes permisos de administrador.")
                    else:
                        st.warning("⚠️ Por favor completa todos los campos.")
    else:
        # Mostrar logout en sidebar cuando está logueado
        with st.sidebar:
            st.markdown("---")
            st.success("✅ Sesión activa como Admin")
            if st.button("🚪 Cerrar Sesión"):
                logout_admin()
                st.rerun()

        show_admin_dashboard()

# Footer (mantener)
try:
    with open("assets/images/beyond2.png", "rb") as f:
        logo_data = base64.b64encode(f.read()).decode()
except Exception:
    logo_data = ""

try:
    with open("assets/images/muyu_logo_blanco_trans.png", "rb") as f:
        muyu_logo_data = base64.b64encode(f.read()).decode()
except Exception:
    muyu_logo_data = ""

footer_original = f"""
<link href="https://fonts.googleapis.com/css2?family=Roboto+Condensed:wght@400;700&display=swap" rel="stylesheet">
<style>
.footer-original {{
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100vw;
    background-color: #4B3C8A;
    color: white;
    padding: 12px 0 8px 0;
    font-size: 12px;
    z-index: 9999;
    font-family: 'Roboto Condensed', Arial, sans-serif !important;
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
.footer-divider {{
    width: 1px;
    background: rgba(255,255,255,0.9);
    height: 56px;
    margin: 0 12px;
}}
</style>
<div class="footer-original">
    <div class="footer-flex" style="display:flex; flex-direction:row; align-items:center; justify-content:space-between; width:100%; gap:32px;">
        <!-- Bloque 1: Logo Beyond Platform -->
        <div style="display:flex; align-items:center; min-width:120px; justify-content:flex-start;">
            <img src="data:image/png;base64,{logo_data}" alt="Beyond Logo" style="height:80px; vertical-align: middle;">
        </div>
        <!-- Divider between Bloque 1 and Bloque 2 -->
        <div class="footer-divider" aria-hidden="true"></div>
        <!-- Bloque 2: Beyond Platform es... + logo Muyu -->
    <div style="display:flex; flex-direction:column; align-items:center; min-width:180px; gap:0; transform: translateY(26px);">
            <span style="color:white; font-size:12px; font-family:'Roboto Condensed', Arial, sans-serif; text-align:center; margin:10; line-height:1;">Beyond Platform es<br>parte de Muyu Education.</span>
            <img src="data:image/png;base64,{muyu_logo_data}" alt="Muyu Logo" style="height:auto; max-height:96px; margin-top:0; object-fit:contain; transform: translateY(-25px);">
        </div>
        <!-- Bloque 3: Sigue a Beyond + iconos -->
        <div style="display:flex; flex-direction:column; align-items:center; min-width:180px;">
            <span style="color:white; font-size:12px; font-family:'Roboto Condensed', Arial, sans-serif; text-align:center;">Sigue a Beyond</span>
            <div style="display:flex; flex-direction:row; align-items:center; justify-content:center; gap:12px; margin-top:6px; margin-bottom:6px;">
                <a href="https://www.linkedin.com/in/tu-perfil-linkedin" target="_blank" title="LinkedIn" style="color: white; text-decoration: none; display:inline-flex; align-items:center;">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="20" height="20"><path fill="white" d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-10h3v10zm-1.5-11.268c-.966 0-1.75-.784-1.75-1.75s.784-1.75 1.75-1.75 1.75.784 1.75 1.75-.784 1.75-1.75 1.75zm15.5 11.268h-3v-5.604c0-1.337-.025-3.063-1.868-3.063-1.868 0-2.154 1.459-2.154 2.968v5.699h-3v-10h2.881v1.367h.041c.401-.761 1.379-1.563 2.838-1.563 3.036 0 3.6 2.001 3.6 4.601v5.595z"/></svg>
                </a>
                <a href="https://www.instagram.com/muyueducation/" target="_blank" title="Instagram" style="color: white; text-decoration: none; display:inline-flex; align-items:center;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" y1="6.5" x2="17.5" y2="6.5"/></svg>
                </a>
            </div>
        </div>
        <!-- Bloque 4: Copyright -->
        <div style="display:flex; align-items:center; min-width:180px; justify-content:flex-end;">
            <span style="color:white; font-size:12px; font-family:'Roboto Condensed', Arial, sans-serif; text-align:right;">&copy; 2025 Beyond Platform - Todos los derechos reservados.</span>
        </div>
    </div>
</div>
"""
st.markdown(footer_original, unsafe_allow_html=True)