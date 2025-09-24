import streamlit as st
import sqlite3
import os
from passlib.context import CryptContext

# Import dashboards
from dashboards import videos_dashboard, podcasts_dashboard, beyond_summit_dashboard, admin_dashboard

# Configuración de la página
st.set_page_config(page_title="Beyond Platform", layout="wide")

# Configuración de la base de datos
DB_NAME = "db/beyond_platform.db"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def get_user_by_email(conn, email: str):
    cur = conn.cursor()
    # Update the query to use 'username' instead of 'email'
    cur.execute("SELECT * FROM usuarios WHERE username = ?", (email,))
    return cur.fetchone()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Crear menú de navegación superior con texto clickeable
col1, col2, col3 = st.columns([1, 1.5, 3], gap="small")
col1.image("assets/images/Beyond_logo.jpg", width=150)
col2.subheader("")
with col3:
    # CSS para estilizar los botones como enlaces de texto
    st.markdown("""
    <style>
    .stButton > button {
        background-color: transparent !important;
        border: none !important;
        color: #1f77b4 !important;
        text-decoration: none !important;
        cursor: pointer !important;
        font-weight: normal !important;
        padding: 0 !important;
        font-size: 16px !important;
        font-family: 'Georgia', 'Times New Roman', serif !important;
        box-shadow: none !important;
    }
    .stButton > button:hover {
        color: red !important;
        background-color: transparent !important;
        border: 1px solid blue !important;
        box-shadow: none !important;
    }
    .stButton > button:focus {
        outline: none !important;
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
    .stButton > button:active {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

    with st.container():
        col1, col2, col3, col4 = st.columns([1,1,1,1])
        with col1:
            if st.button("Videos", key="videos_nav"):
                st.session_state.page = "videos"
                st.rerun()
        with col2:
            if st.button("Podcasts", key="podcasts_nav"):
                st.session_state.page = "podcasts"
                st.rerun()
        with col3:
            if st.button("Beyond Summit", key="beyond_summit_nav"):
                st.session_state.page = "beyond_summit"
                st.rerun()
        with col4:
            if st.button("Admin space", key="admin_space_nav"):
                st.session_state.page = "admin"
                st.rerun()

# Diseño con elementos pegados a los lados y más cerca entre sí
with st.container():
    col1, col2, col3, col4 = st.columns([.4,2.6,2,.2], gap="small")

    with col2:
        st.video("https://www.youtube.com/embed/ZNn2MBdliow")

    with col3:
    
        st.image("assets/images/beyond_platform1.jpg", width=390)
    

# Navegación entre dashboards
if "page" not in st.session_state:
    st.session_state.page = "videos"  # Página predeterminada

if st.session_state.page == "videos":
    videos_dashboard.show()
elif st.session_state.page == "podcasts":
    podcasts_dashboard.show()
elif st.session_state.page == "beyond_summit":
    beyond_summit_dashboard.show()
elif st.session_state.page == "admin":
    if "admin_logged_in" not in st.session_state or not st.session_state.admin_logged_in:
        st.title("Admin Login")
        with st.form("admin_login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
            if submitted:
                conn = get_db()
                user = get_user_by_email(conn, email)
                conn.close()
                if user and user["rol"] == "admin" and verify_password(password, user["password"]):
                    st.session_state.admin_logged_in = True
                    st.success("Login exitoso. Bienvenido al Admin Space.")
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas o no tienes permisos de administrador.")
    else:
        admin_dashboard.show()

# Footer con color violeta
st.markdown("""
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #7c73e6;
    color: white;
    text-align: center;
    padding: 10px 0;
    z-index: 999;
    font-family: 'Arial', sans-serif;
}
</style>
<div class="footer">
    <p>© 2025 Beyond Platform | Todos los derechos reservados | Política de privacidad | Términos de servicio</p>
</div>
""", unsafe_allow_html=True)
