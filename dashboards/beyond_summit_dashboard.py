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
    # Add custom CSS for styling
    st.markdown("""
    <style>
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: pointer;
    }

    .tooltip .tooltiptext {
        visibility: hidden;
        width: 300px;
        background-color: #333;
        color: white;
        text-align: left;
        border-radius: 6px;
        padding: 10px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -150px;
        opacity: 0;
        transition: opacity 0.3s;
        font-size: 14px;
        line-height: 1.4;
        box-shadow: 0px 0px 10px rgba(0,0,0,0.3);
    }

    .tooltip .tooltiptext::after {
        content: "";
        position: absolute;
        top: 100%;
        left: 50%;
        margin-left: -5px;
        border-width: 5px;
        border-style: solid;
        border-color: #333 transparent transparent transparent;
    }

    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    
    .summit-hero {
        background: linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 100%);
        border-radius: 15px;
        padding: 25px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
    }
    
    .event-card {
        border: 2px solid #e0e0e0;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        background: linear-gradient(145deg, #f8f9fa 0%, #e9ecef 100%);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    
    .event-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    
    .event-status {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    
    .status-upcoming {
        background-color: #28a745;
        color: white;
    }
    
    .status-live {
        background-color: #dc3545;
        color: white;
        animation: pulse 1.5s infinite;
    }
    
    .status-completed {
        background-color: #6c757d;
        color: white;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    </style>
    """, unsafe_allow_html=True)

    # Get all events from database
    conn = get_db()
    c = conn.cursor()
    
    # Check if likes column exists, if not add it
    try:
        c.execute("SELECT * FROM beyond_summit ORDER BY likes DESC, titulo ASC")
        events = c.fetchall()
    except sqlite3.OperationalError:
        # Add likes column if it doesn't exist
        try:
            c.execute("ALTER TABLE beyond_summit ADD COLUMN likes INTEGER DEFAULT 0")
            conn.commit()
            c.execute("SELECT * FROM beyond_summit ORDER BY likes DESC, titulo ASC")
            events = c.fetchall()
        except sqlite3.OperationalError:
            # Table might not exist
            events = []
    
    conn.close()

    # Find the event with most likes (first one after ordering)
    main_event = events[0] if events else None
    
    col1, col2 = st.columns([3, 6])
    with col1: 
        # Introductory paragraph about Beyond Summit
        st.markdown("""
            **🚀 Beyond Summit Experience**  
            
            Únete a experiencias transformadoras que van más allá de lo convencional. 
            Nuestros eventos conectan líderes visionarios, innovadores y mentes creativas 
            en conversaciones que inspiran el cambio y el crecimiento.
            
            **✨ Lo que te espera:**
            - Conferencias magistrales
            - Workshops interactivos  
            - Networking exclusivo
            - Experiencias inmersivas
        """)
    with col2:
        if main_event:
            # Show the most liked event as main event
            event_status = main_event.get('estado', 'upcoming')
            status_class = f"status-{event_status}"
            status_text = {
                'upcoming': '🔜 PRÓXIMO',
                'live': '🔴 EN VIVO',
                'completed': '✅ COMPLETADO'
            }.get(event_status, '🔜 PRÓXIMO')
            
            st.markdown(f"""
                <div class="summit-hero">
                    <div class="event-status {status_class}">{status_text}</div>
                    <h2>🎯 Evento Destacado</h2>
                    <h3>{main_event['titulo']}</h3>
                    <p><strong>📅 Fecha:</strong> {main_event.get('fecha', 'Por confirmar')}</p>
                    <p><strong>⏰ Hora:</strong> {main_event.get('hora', 'Por confirmar')}</p>
                    <p><strong>❤️ {main_event.get('likes', 0)} personas interesadas</strong></p>
                </div>
            """, unsafe_allow_html=True)
        else:
            # Fallback message if no events in database
            st.markdown("""
                <div class="summit-hero">
                    <h2>🎯 Próximos Eventos</h2>
                    <p>Estamos preparando experiencias extraordinarias para ti.</p>
                    <p><strong>¡Mantente conectado para las próximas fechas!</strong></p>
                    <br>
                    <p>🔔 Activa las notificaciones</p>
                    <p>📧 Suscríbete a nuestro newsletter</p>
                </div>
            """, unsafe_allow_html=True)

    # Add separator line between introduction and events
    st.markdown("---")

    if events:
        st.subheader("🗓️ Todos los Eventos Beyond Summit")
        
        for i, event in enumerate(events):
            # Determine event status and styling
            event_status = event.get('estado', 'upcoming')
            status_class = f"status-{event_status}"
            status_text = {
                'upcoming': '🔜 PRÓXIMO',
                'live': '🔴 EN VIVO',
                'completed': '✅ COMPLETADO'
            }.get(event_status, '🔜 PRÓXIMO')
            
            # Check if description needs truncation
            description = event['descripcion'] or ""
            truncated_desc = truncate_text(description, 200)
            is_truncated = len(description) > 200
            
            # Create tooltip HTML if description is truncated
            if is_truncated:
                description_html = f"""
                <div class="tooltip">
                    <span>{truncated_desc}</span>
                    <span class="tooltiptext">{description}</span>
                </div>
                """
            else:
                description_html = truncated_desc
            
            # Event card
            st.markdown(f"""
                <div class="event-card">
                    <div class="event-status {status_class}">{status_text}</div>
                    <h3 style="color: #2c3e50; margin-bottom: 15px;">🎤 {event['titulo']}</h3>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 15px;">
                        <div>
                            <p style="margin: 5px 0;"><strong>📅 Fecha:</strong> {event.get('fecha', 'Por confirmar')}</p>
                            <p style="margin: 5px 0;"><strong>⏰ Hora:</strong> {event.get('hora', 'Por confirmar')}</p>
                        </div>
                        <div>
                            <p style="margin: 5px 0;"><strong>📍 Lugar:</strong> {event.get('lugar', 'Virtual/Presencial')}</p>
                            <p style="margin: 5px 0;"><strong>👥 Ponente:</strong> {event.get('ponente', 'Por anunciar')}</p>
                        </div>
                    </div>
                    <p style="color: #666; font-size: 14px; line-height: 1.5; margin-bottom: 15px;">{description_html}</p>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <small style="color: #888;">🏷️ Categoría: {event.get('categoria', 'Conferencia')}</small>
                        <small style="color: #888;">💰 {event.get('precio', 'Gratuito')}</small>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Action buttons
            col1, col2, col3 = st.columns(3)
            with col1:
                likes_count = event.get('likes', 0) or 0
                if st.button(f"❤️ Me interesa ({likes_count})", key=f"like_{event['id']}"):
                    like_event(event['id'])
                    st.rerun()
            with col2:
                if event_status == 'upcoming':
                    if st.button("📝 Registrarse", key=f"register_{event['id']}"):
                        registration_url = register_for_event(event['id'])
                        st.success("¡Registro exitoso! Te enviaremos los detalles por email.")
                        st.info("🔗 Link de confirmación enviado a tu email")
                elif event_status == 'live':
                    if st.button("🔴 Unirse Ahora", key=f"join_{event['id']}"):
                        st.success("¡Redirigiendo al evento en vivo!")
                else:  # completed
                    if st.button("📹 Ver Grabación", key=f"watch_{event['id']}"):
                        st.info("Accediendo a la grabación del evento...")
            with col3:
                if st.button("📤 Compartir", key=f"share_{event['id']}"):
                    share_url = get_share_url(event.get('url', '#'))
                    st.success(f"¡Comparte este evento!")
                    st.code(f"🔗 {share_url}")
            
            # Add separator between events
            if i < len(events) - 1:
                st.markdown("---")
                
    else:
        st.info("🎪 No hay eventos programados en este momento. ¡Grandes cosas están por venir!")
        
        # Call to action section when no events available
        st.markdown("""
        ### 🌟 Mientras preparamos eventos increíbles...
        
        **📧 Mantente conectado:**
        - Suscríbete a nuestro newsletter para recibir anuncios exclusivos
        - Síguenos en redes sociales para actualizaciones en tiempo real
        - Únete a nuestra comunidad para ser el primero en conocer las fechas
        
        **🎥 Explora nuestro contenido:**
        - **Videos** inspiradores de eventos pasados
        - **Podcasts** con conversaciones profundas de nuestros speakers
        
        **💡 ¿Tienes ideas para eventos?**
        ¡Nos encantaría escucharte! Contáctanos para proponer temas o speakers.
        """)
        
        # Newsletter signup placeholder
        with st.expander("📬 Suscríbete para recibir notificaciones"):
            email = st.text_input("Tu email", placeholder="ejemplo@email.com")
            interests = st.multiselect(
                "Temas de interés:",
                ["Tecnología", "Liderazgo", "Innovación", "Emprendimiento", "Desarrollo Personal"]
            )
            if st.button("🔔 Suscribirse"):
                if email:
                    st.success("¡Gracias! Te notificaremos sobre próximos eventos.")
                else:
                    st.error("Por favor, ingresa tu email.")
