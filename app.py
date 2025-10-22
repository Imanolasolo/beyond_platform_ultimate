import streamlit as st
import base64

# Configurar la página
st.set_page_config(
    page_title="Beyond Summit",
    page_icon=":guardsman:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inyectar Roboto Condensed (solo el link, estilos específicos se definen más abajo)
st.markdown('<link href="https://fonts.googleapis.com/css2?family=Roboto+Condensed:wght@400;700&display=swap" rel="stylesheet">', unsafe_allow_html=True)

# Definición del menú (etiqueta visible, slug para query param)
menu_items = [
    ("**¿QUÉ ES BEYOND PLATFORM?**", "init"),
    ("**CHARLAS**", "charlas"),
    ("**PODCASTS**", "podcasts"),
    ("**BEYOND SUMMIT**", "summit"),
    ("**INICIAR SESION**", "admin"),  # nueva opción añadida
]
label_to_slug = {label: slug for label, slug in menu_items}
slug_to_label = {slug: label for label, slug in menu_items}
menu_options = [label for label, _ in menu_items]

# Leer query params directamente y determinar el slug (sin session_state)
try:
    params = st.query_params or {}
except Exception:
    params = {}

menu_param_raw = params.get("menu")
if isinstance(menu_param_raw, list):
    menu_slug = menu_param_raw[0] if menu_param_raw else None
else:
    menu_slug = menu_param_raw

# Normalizar y validar el slug; usar 'init' por defecto
if not menu_slug or menu_slug not in slug_to_label:
    menu_slug = 'init'

# Determinar la etiqueta seleccionada a partir del slug (fuente de verdad = URL)
selected_label = slug_to_label[menu_slug]

# Cabecera en barra gris full-width que contiene logo y menú
current_menu = selected_label
# No session helpers: navigation se basa únicamente en ?menu=slug en la URL

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
    # links normales usando href (dejar que el navegador recarge y Streamlit actualice query params)
    menu_links_html += (
        f'<a href="?menu={slug}" '
        f'class="custom-menu-link {selected_class}">{link_text}</a>'
    )

st.markdown(f'''
<style>
    .top-bar {{
        position: relative;
        left: -80px;
        right: -80px;
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

selected = selected_label

# Importar dashboards
from dashboards.videos_dashboard import show as show_videos_dashboard
from dashboards.podcasts_dashboard import show as show_podcasts_dashboard
from dashboards.beyond_summit_dashboard import show as show_beyond_summit_dashboard
from dashboards.init_dashboard import show as show_init_dashboard
from dashboards.admin_dashboard1 import show as show_admin_dashboard1  # import añadido

# Mostrar el dashboard correspondiente según la opción seleccionada
if selected == "**¿QUÉ ES BEYOND PLATFORM?**":
    show_init_dashboard()
elif selected == "**CHARLAS**":
    show_videos_dashboard()
elif selected == "**PODCASTS**":
    show_podcasts_dashboard()
elif selected == "**BEYOND SUMMIT**":
    show_beyond_summit_dashboard()
elif selected == "**INICIAR SESION**":  # manejo de la nueva opción
    show_admin_dashboard1()

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