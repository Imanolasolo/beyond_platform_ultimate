import sqlite3
import streamlit as st
from datetime import datetime

DB_NAME = "db/beyond_platform.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def truncate_text(text, max_length=100):
    """Truncate text to a maximum length with ellipsis."""
    return text if len(text) <= max_length else text[:max_length] + "..."

def like_event(event_id):
    """Increment the like count for an event."""
    conn = get_db()
    c = conn.cursor()
    try:
        # Try to update likes column, if it doesn't exist, add it first
        c.execute("UPDATE beyond_summit SET likes = likes + 1 WHERE id = ?", (event_id,))
    except sqlite3.OperationalError:
        # Add likes column if it doesn't exist
        c.execute("ALTER TABLE beyond_summit ADD COLUMN likes INTEGER DEFAULT 0")
        c.execute("UPDATE beyond_summit SET likes = likes + 1 WHERE id = ?", (event_id,))
    conn.commit()
    conn.close()

def register_for_event(event_id):
    """Handle event registration (placeholder function)."""
    return f"Registration link for event {event_id}"

def get_share_url(event_url):
    """Generate a shareable URL for the event."""
    return event_url

def show():
    # CSS y layout similar a init_dashboard.py, sin video hero
    st.markdown("""
    <link href='https://fonts.googleapis.com/css2?family=Roboto+Condensed:wght@700&display=swap' rel='stylesheet'>
    <style>
    .beyond-title-hero {
        font-size: 40px;
        font-weight: bold;
        color: #7c82ce;
        text-align: center;
        margin-bottom: 0px;
        margin-top: 24px;
        letter-spacing: 0.01em;
        font-family: 'Roboto Condensed', Arial, sans-serif;
    }
    .fullwidth-row {
        width: 100vw;
        min-width: 100vw;
        max-width: 100vw;
        margin-left: calc(-50vw + 50%);
        margin-right: calc(-50vw + 50%);
        box-sizing: border-box;
        display: flex;
        flex-direction: row;
        padding: 0;
        gap: 0;
        background: transparent;
    }
    .fullwidth-row > div {
        flex: 1 1 0;
        min-width: 0;
        padding: 0;
        margin: 0;
    }
    .fullwidth-row img {
        display: block;
        width: 100%;
        height: 60vh;
        max-height: 90vh;
        border-radius: 0;
        margin: 0;
        padding: 0;
        object-fit: cover;
        background: #eee;
    }
    @media (max-width: 900px) {
        .fullwidth-row img {
            height: 40vh;
        }
    }
    @media (max-width: 600px) {
        .fullwidth-row {
            flex-direction: column;
        }
        .fullwidth-row img {
            height: 30vh;
        }
    }
    .info-box-below-hero {
        width: 100vw;
        min-width: 100vw;
        max-width: 100vw;
        margin-left: calc(-50vw + 50%);
        margin-right: calc(-50vw + 50%);
        background: #f4f5fa;
        display: flex;
        flex-direction: row;
        gap: 0;
        border-radius: 0 0 16px 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        padding: 0;
        margin-top: 0;
        margin-bottom: 0;
    }
    .info-box-below-hero > div {
        flex: 1 1 0;
        padding: 32px 40px 32px 40px;
        font-size: 1.15rem;
        color: #444;
        line-height: 1.6;
        background: none;
        margin: 0;
        display: flex;
        flex-direction: column;
        justify-content: center;
        height: 100%;
    }
    .info-box-below-hero > div:first-child {
        align-items: center;
        flex-basis: 40%;
        max-width: 40%;
    }
    .info-box-below-hero > div:last-child {
        align-items: center;
        justify-content: center;
        flex-basis: 60%;
        max-width: 60%;
        text-align: center;
    }
    @media (max-width: 900px) {
        .info-box-below-hero {
            flex-direction: column;
        }
        .info-box-below-hero > div {
            padding: 18px 10px 18px 10px;
            flex-basis: 100%;
            max-width: 100%;
            align-items: center !important;
        }
    }
    @media (max-width: 900px) {
        .info-box-below-hero > div {
            padding: 18px 10px 18px 10px;
        }
    }
    .summit-card {
        background: #fff;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.07);
        padding: 12px 8px 18px 8px;
        margin-bottom: 18px;
        display: flex;
        flex-direction: column;
        align-items: center;
        min-height: 220px;
    }
    .summit-card-title {
        font-size: 1.1rem;
        font-weight: bold;
        color: #333;
        text-align: center;
        margin-top: 6px;
        font-family: 'Roboto Condensed', Arial, sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

    # Imagen destacada (puedes cambiar la ruta si tienes una imagen específica)
    import os, base64
    local_img = "assets/images/image1.jpg"
    if os.path.exists(local_img):
        with open(local_img, "rb") as img_file:
            img_base64 = base64.b64encode(img_file.read()).decode()
        img_src = f"data:image/jpeg;base64,{img_base64}"
    else:
        img_src = "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80"

    titulo_html = "<span class='beyond-title-hero'>BEYOND SUMMIT</span>"
    # Info box centrada usando columnas de Streamlit
    st.markdown(f"""
    <div class="fullwidth-row">
        <div>
            <img src="{img_src}" alt="Imagen Beyond Summit" />
        </div>
        <div style="display:flex; align-items:center; justify-content:center;">
            {titulo_html}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Caja gris con texto centrado usando columnas
    # Solo caja gris con texto centrado usando columnas de Streamlit
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown(
            """
            <div style='background:#f4f5fa; border-radius:0 0 16px 16px; box-shadow:0 2px 8px rgba(0,0,0,0.04); padding:32px 40px; font-size:1.15rem; color:#444; line-height:1.6; text-align:center;'>
            Beyond Summit es el espacio donde conectamos líderes, innovadores y mentes creativas en experiencias transformadoras.<br>
            Conferencias, workshops, networking y más para inspirar el cambio y el crecimiento.
            </div>
            """,
            unsafe_allow_html=True
        )

    # Obtener eventos de la base de datos
    conn = get_db()
    c = conn.cursor()
    try:
        c.execute("SELECT * FROM beyond_summit ORDER BY likes DESC, titulo ASC")
        events = c.fetchall()
    except sqlite3.OperationalError:
        try:
            c.execute("ALTER TABLE beyond_summit ADD COLUMN likes INTEGER DEFAULT 0")
            conn.commit()
            c.execute("SELECT * FROM beyond_summit ORDER BY likes DESC, titulo ASC")
            events = c.fetchall()
        except sqlite3.OperationalError:
            events = []
    conn.close()

    st.markdown('<div style="font-size:2rem; color:#7c82ce; font-weight:bold; text-decoration:underline; font-family:Roboto Condensed,Arial,sans-serif; margin:32px 0 18px 0; text-align:left;">Eventos Beyond Summit</div>', unsafe_allow_html=True)

    if events:
        cols = st.columns(4)
        for idx, event in enumerate(events):
            with cols[idx % 4]:
                st.markdown(f"""
                    <div class='summit-card'>
                        <div class='summit-card-title'>{event['titulo']}</div>
                        <div style='font-size:0.95rem; color:#666; margin:8px 0 4px 0;'>
                            <strong>📅 Fecha:</strong> {event.get('fecha', 'Por confirmar')}<br>
                            <strong>⏰ Hora:</strong> {event.get('hora', 'Por confirmar')}<br>
                            <strong>📍 Lugar:</strong> {event.get('lugar', 'Virtual/Presencial')}<br>
                            <strong>👥 Ponente:</strong> {event.get('ponente', 'Por anunciar')}
                        </div>
                        <div style='font-size:0.9rem; color:#888; margin-bottom:8px;'>
                            {truncate_text(event['descripcion'] or '', 120)}
                        </div>
                        <div style='display:flex; justify-content:center; gap:10px; margin-top:auto;'>
                            <span style='font-size:0.9rem; color:#7c82ce;'>❤️ {event.get('likes', 0) or 0}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                if st.button(f"❤️ Me interesa ({event.get('likes', 0) or 0})", key=f"like_{event['id']}"):
                    like_event(event['id'])
                    st.rerun()

    if events:
        st.subheader("🗓️ Todos los Eventos Beyond Summit")
        
        for i, event in enumerate(events):
            # ...existing code...
            if i < len(events) - 1:
                st.markdown("---")
    else:
        st.info("No hay eventos programados en este momento. ¡Grandes cosas están por venir!")
        # Call to action section when no events available
        st.markdown("""
        ### Mientras preparamos eventos increíbles...
        
        **Mantente conectado:**
        - Suscríbete a nuestro newsletter para recibir anuncios exclusivos
        - Síguenos en redes sociales para actualizaciones en tiempo real
        - Únete a nuestra comunidad para ser el primero en conocer las fechas
        
        **Explora nuestro contenido:**
        - **Videos** inspiradores de eventos pasados
        - **Podcasts** con conversaciones profundas de nuestros speakers
        
        **¿Tienes ideas para eventos?**
        ¡Nos encantaría escucharte! Contáctanos para proponer temas o speakers.
        """)
        # Newsletter signup placeholder
        with st.expander("Suscríbete para recibir notificaciones"):
            email = st.text_input("Tu email", placeholder="ejemplo@email.com")
            interests = st.multiselect(
                "Temas de interés:",
                ["Tecnología", "Liderazgo", "Innovación", "Emprendimiento", "Desarrollo Personal"]
            )
            if st.button("Suscribirse"):
                if email:
                    st.success("¡Gracias! Te notificaremos sobre próximos eventos.")
                else:
                    st.error("Por favor, ingresa tu email.")
