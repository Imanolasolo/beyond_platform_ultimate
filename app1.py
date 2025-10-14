import streamlit as st
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

# Inyectar Roboto Condensed desde Google Fonts y aplicarlo al menú
st.markdown('''
    <link href="https://fonts.googleapis.com/css2?family=Roboto+Condensed:wght@700&display=swap" rel="stylesheet">
    <style>
    .roboto-expanded * {
        font-family: 'Roboto Condensed', Arial, sans-serif !important;
        letter-spacing: 0.04em;
        font-stretch: expanded;
    }
    /* Ocultar cualquier icono, flecha o chevron del menu superior option_menu */
    .option-menu-horizontal .menu-icon,
    .option-menu-horizontal .nav-link .fa,
    .option-menu-horizontal .nav-link .bi,
    .option-menu-horizontal .nav-link svg,
    .option-menu-horizontal .nav-link i,
    .option-menu-horizontal .nav-link [class*="icon"],
    .option-menu-horizontal .nav-link [class*="chevron"],
    .option-menu-horizontal .nav-link [class*="arrow"],
    .option-menu-horizontal .nav-link [data-testid*="icon"],
    .option-menu-horizontal .nav-link [data-testid*="chevron"],
    .option-menu-horizontal .nav-link [data-testid*="arrow"],
    .option-menu-horizontal .nav-link > span > svg,
    .option-menu-horizontal .nav-link > svg,
    .option-menu-horizontal .nav-link > i {
        display: none !important;
    }
    /* También ocultar cualquier icono en el contenedor del menú */
    .option-menu-horizontal [class*="icon"],
    .option-menu-horizontal [class*="chevron"],
    .option-menu-horizontal [class*="arrow"] {
        display: none !important;
    }
    /* Ocultar pseudo-elementos ::after y ::before en los enlaces del menú */
    .option-menu-horizontal .nav-link::after,
    .option-menu-horizontal .nav-link::before {
        display: none !important;
        content: none !important;
    }
    /* Ocultar cualquier <i> o <svg> dentro de los enlaces del menú */
    .option-menu-horizontal .nav-link i,
    .option-menu-horizontal .nav-link svg {
        display: none !important;
    }
    /* Forzar solo texto en el menú */
    .option-menu-horizontal .nav-link span.menu-icon {
        display: none !important;
    }
    </style>
''', unsafe_allow_html=True)

menu_options = ["**¿QUÉ ES BEYOND PLATFORM?**", "**CHARLAS**", "**PODCASTS**", "**BEYOND SUMMIT**", "**INICIAR SESIÓN**"]
if 'selected_menu' not in st.session_state:
    st.session_state.selected_menu = menu_options[0]

col1, col2, col3 = st.columns([1, 1, 3])
with col1:
# Menú superior solo HTML y CSS, sin columnas ni botones
    st.image('assets/images/beyond1.png', width=200)



with col3:
# Menú superior con navegación instantánea usando st.button y CSS para que parezcan links
    current_menu = st.session_state.selected_menu
    st.markdown('''
        <style>
        .custom-menu-row {
            display: flex;
            flex-direction: row;
            justify-content: center;
            align-items: center;
            gap: 0;
            margin-bottom: 8px;
            border-bottom: 1px solid #e0e0e0;
            background: transparent;
        }
        .custom-menu-btn {
            font-family: 'Roboto Condensed', Arial, sans-serif !important;
            font-size: 14px;
            color: #222 !important;
            background: none !important;
            border: none !important;
            outline: none !important;
            box-shadow: none !important;
            padding: 6px 0 8px 0;
            margin: 0 2px;
            cursor: pointer;
            transition: color 0.2s, border-bottom 0.2s, background 0.2s;
            border-bottom: 2px solid transparent;
            font-weight: 700 !important;
            font-weight: bold !important;
            letter-spacing: 0.04em;
            text-decoration: none;
            display: inline-block;
        }
        .custom-menu-btn.selected {
            color: #7B2FF2 !important;
            border-bottom: 2px solid #7B2FF2 !important;
        }
        .custom-menu-btn:hover,
        .custom-menu-btn:focus-visible,
        .custom-menu-btn:active {
            color: #fff !important;
            background: #7B2FF2 !important;
            border-bottom: 2px solid #7B2FF2 !important;
        }
        /* Forzar el fondo de los botones de Streamlit a transparente */
        div[data-testid="stButton"] button {
            background: transparent !important;
            border: none !important;
            outline: none !important;
            box-shadow: none !important;
            color: inherit !important;
            width: 100%;
            height: auto;
            padding: 0;
            margin: 0;
            min-width: 0;
            min-height: 0;
        }
        </style>
    ''', unsafe_allow_html=True)
    import streamlit as __st
    menu_cols = st.columns(len(menu_options), gap="small")
    for idx, option in enumerate(menu_options):
        btn_class = "custom-menu-btn selected" if current_menu == option else "custom-menu-btn"
        with menu_cols[idx]:
            btn = st.button(option, key=f"menu_{option}")
            if btn:
                st.session_state.selected_menu = option
    selected = st.session_state.selected_menu

# Importar los dashboards
from dashboards.videos_dashboard import show as show_videos_dashboard
from dashboards.podcasts_dashboard import show as show_podcasts_dashboard
from dashboards.admin_dashboard import show as show_admin_dashboard
from dashboards.beyond_summit_dashboard import show as show_beyond_summit_dashboard 
from dashboards.init_dashboard import show as show_init_dashboard

# Reset admin login when navigating away from Iniciar sesión
if selected != "**INICIAR SESIÓN**" and "admin_logged_in" in st.session_state:
    del st.session_state.admin_logged_in

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
                            st.session_state.selected_menu = "**INICIAR SESIÓN**"
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

with open("assets/images/beyond2.png", "rb") as f:
    logo_data = base64.b64encode(f.read()).decode()
with open("assets/images/muyu_logo_blanco_trans.png", "rb") as f:
    muyu_logo_data = base64.b64encode(f.read()).decode()

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
</style>
<div class="footer-original">
    <div class="footer-flex" style="display:flex; flex-direction:row; align-items:center; justify-content:space-between; width:100%; gap:32px;">
        <!-- Bloque 1: Logo Beyond Platform -->
        <div style="display:flex; align-items:center; min-width:120px; justify-content:flex-start;">
            <img src="data:image/png;base64,{logo_data}" alt="Beyond Logo" style="height:50px; vertical-align: middle;">
        </div>
        <!-- Bloque 2: Beyond Platform es... + logo Muyu -->
        <div style="display:flex; flex-direction:column; align-items:center; min-width:180px;">
            <span style="color:white; font-size:12px; font-family:'Roboto Condensed', Arial, sans-serif; text-align:center;">Beyond Platform es<br>parte de Muyu Education.</span>
            <img src="data:image/png;base64,{muyu_logo_data}" alt="Muyu Logo" style="height:auto; max-height:72px; margin-top:0; object-fit:contain;">
        </div>
        <!-- Bloque 3: Sigue a Beyond + iconos -->
        <div style="display:flex; flex-direction:column; align-items:center; min-width:180px;">
            <span style="color:white; font-size:12px; font-family:'Roboto Condensed', Arial, sans-serif; text-align:center;">Sigue a Beyond</span>
            <div style="display:flex; flex-direction:row; align-items:center; justify-content:center; gap:12px; margin-top:2px; margin-bottom:2px;">
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
            <span style="color:white; font-size:12px; font-family:'Roboto Condensed', Arial, sans-serif; text-align:right;">&copy; 2024 Beyond Platform - Todos los derechos reservados.</span>
        </div>
    </div>
</div>
"""
st.markdown(footer_original, unsafe_allow_html=True)