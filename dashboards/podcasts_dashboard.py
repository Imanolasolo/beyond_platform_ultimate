import sqlite3
import streamlit as st

DB_NAME = "db/beyond_platform.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def truncate_text(text, max_length=100):
    """Truncate text to a maximum length with ellipsis."""
    return text if len(text) <= max_length else text[:max_length] + "..."

def like_podcast(podcast_id):
    """Increment the like count for a podcast."""
    conn = get_db()
    c = conn.cursor()
    try:
        # Try to update likes column, if it doesn't exist, add it first
        c.execute("UPDATE podcasts SET likes = likes + 1 WHERE id = ?", (podcast_id,))
    except sqlite3.OperationalError:
        # Add likes column if it doesn't exist
        c.execute("ALTER TABLE podcasts ADD COLUMN likes INTEGER DEFAULT 0")
        c.execute("UPDATE podcasts SET likes = likes + 1 WHERE id = ?", (podcast_id,))
    conn.commit()
    conn.close()

def get_share_url(podcast_url):
    """Generate a shareable URL for the podcast."""
    return podcast_url

def show():
    # Add custom CSS for tooltip
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
    
    .podcast-player {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 20px;
        color: white;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

    # Get all podcasts from database
    conn = get_db()
    c = conn.cursor()
    
    # Check if likes column exists, if not add it
    try:
        c.execute("SELECT * FROM podcasts ORDER BY likes DESC, titulo ASC")
        podcasts = c.fetchall()
    except sqlite3.OperationalError as e:
        try:
            # Add likes column if it doesn't exist
            c.execute("ALTER TABLE podcasts ADD COLUMN likes INTEGER DEFAULT 0")
            conn.commit()
            c.execute("SELECT * FROM podcasts ORDER BY likes DESC, titulo ASC")
            podcasts = c.fetchall()
        except sqlite3.OperationalError:
            # Table might not exist
            podcasts = []
            st.error("Error: La tabla de podcasts no existe en la base de datos.")
    
    conn.close()

    # Find the podcast with most likes (first one after ordering)
    main_podcast = podcasts[0] if podcasts else None
    
    col1, col2 = st.columns([3, 6])
    with col1: 
        # Introductory paragraph about Podcasts
        st.markdown("""
            **Descubre Nuestros Podcasts**  
            Sumérgete en conversaciones profundas y reflexivas con expertos de diversas áreas. 
            Nuestros podcasts están diseñados para expandir tu mente, inspirar nuevas ideas y 
            acompañarte en tu crecimiento personal y profesional.
        """)
    with col2:
        if main_podcast:
            # Show the most liked podcast as main podcast
            st.markdown(f"""
                <div class="podcast-player">
                    <h3>🎧 Podcast Más Popular</h3>
                    <h4>{main_podcast['titulo']}</h4>
                    <audio controls style="width: 100%; margin: 10px 0;">
                        <source src="{main_podcast['url']}" type="audio/mpeg">
                        Tu navegador no soporta el elemento de audio.
                    </audio>
                    <p style="font-style: italic; margin-top: 10px;">
                        {main_podcast['likes'] or 0} likes | Duración: {main_podcast.get('duracion', 'N/A')}
                    </p>
                </div>
            """, unsafe_allow_html=True)
        else:
            # Fallback message if no podcasts in database
            st.markdown("""
                <div class="podcast-player">
                    <h3>🎧 Próximamente</h3>
                    <p>Estamos preparando contenido increíble para ti.</p>
                    <p>¡Mantente atento a nuestros próximos lanzamientos!</p>
                </div>
            """, unsafe_allow_html=True)

    # Add separator line between introduction and podcasts
    st.markdown("---")

    if podcasts:
        st.subheader("🎙️ Todos los Podcasts")
        
        for i in range(0, len(podcasts), 2):  # Group podcasts in sets of 2 for better layout
            group = podcasts[i:i+2]
            cols = st.columns(2)  # Create 2 columns for the group
            for col, podcast in zip(cols, group):
                with col:
                    # Check if description needs truncation
                    description = podcast['descripcion'] or ""
                    truncated_desc = truncate_text(description, 150)
                    is_truncated = len(description) > 150
                    
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
                    
                    # Podcast card
                    st.markdown(f"""
                        <div style="border: 1px solid #ddd; border-radius: 10px; padding: 15px; margin-bottom: 20px; background-color: #f9f9f9;">
                            <h4 style="color: #333; margin-bottom: 10px;">🎧 {podcast['titulo']}</h4>
                            <audio controls style="width: 100%; margin: 10px 0;">
                                <source src="{podcast['url']}" type="audio/mpeg">
                                Tu navegador no soporta el elemento de audio.
                            </audio>
                            <p style="margin-top: 10px; color: #666; font-size: 14px;">{description_html}</p>
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px;">
                                <small style="color: #888;">Duración: {podcast.get('duracion', 'N/A')}</small>
                                <small style="color: #888;">Categoría: {podcast.get('categoria', 'General')}</small>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Like and Share buttons
                    button_col1, button_col2 = st.columns(2)
                    with button_col1:
                        likes_count = podcast.get('likes', 0) or 0
                        if st.button(f"❤️ Like ({likes_count})", key=f"like_{podcast['id']}"):
                            like_podcast(podcast['id'])
                            st.rerun()
                    with button_col2:
                        if st.button("📤 Share", key=f"share_{podcast['id']}"):
                            share_url = get_share_url(podcast['url'])
                            st.success(f"URL para compartir: {share_url}")
                            st.code(share_url)

            if i + 2 < len(podcasts):  # Add separator between groups, but not after the last group
                st.markdown("---")
    else:
        st.info("📻 No hay podcasts disponibles en este momento. ¡Pronto tendremos contenido increíble para ti!")
        
        # Suggestion section when no podcasts available
        st.markdown("""
        ### 💡 Mientras tanto...
        
        - Explora nuestros **Videos** para contenido visual inspirador
        - Únete a **Beyond Summit** para eventos en vivo
        - Suscríbete para recibir notificaciones de nuevos podcasts
        """)
