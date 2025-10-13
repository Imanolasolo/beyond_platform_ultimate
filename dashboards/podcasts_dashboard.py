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
    # Unificar estilos visuales con la home
    st.markdown("""
    <style>
    .podcasts-title {
        font-size: 24px;
        font-weight: bold;
        color: #7c82ce;
        text-align: left;
        margin-bottom: 20px;
    }
    .podcast-item {
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
        margin-bottom: 15px;
        padding: 15px;
        background-color: #f8f9fa;
    }
    .podcast-item:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    .podcast-title {
        font-size: 16px;
        font-weight: bold;
        color: #333;
        margin-bottom: 8px;
        line-height: 1.3;
    }
    .podcast-desc {
        font-size: 14px;
        color: #555;
        margin-bottom: 10px;
        text-align: center;
    }
    .like-btn {
        background: linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: bold;
        cursor: pointer;
        margin-right: 8px;
    }
    .like-btn:hover {
        background: linear-gradient(135deg, #ff5722 0%, #00bcd4 100%);
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

    # Título principal
    st.markdown('<div class="podcasts-title">PODCASTS</div>', unsafe_allow_html=True)
    st.markdown("---")
    if podcasts:
        # Mostrar podcasts en tarjetas de 4 columnas como en la home
        for i in range(0, len(podcasts), 4):
            group = podcasts[i:i+4]
            cols = st.columns(4)
            for col, podcast in zip(cols, group):
                with col:
                    url = podcast['url']
                    is_youtube = ('youtube.com/watch?v=' in url) or ('youtu.be/' in url)
                    video_embed = ''
                    if is_youtube:
                        if 'youtube.com/watch?v=' in url:
                            video_id = url.split('watch?v=')[-1].split('&')[0]
                        elif 'youtu.be/' in url:
                            video_id = url.split('youtu.be/')[-1].split('?')[0]
                        else:
                            video_id = ''
                        if video_id:
                            video_embed = f'<iframe width="100%" height="180" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="border-radius: 8px; margin-bottom: 10px;"></iframe>'
                    st.markdown(f'''
                    <div class="podcast-item">
                        <div class="podcast-title">{podcast['titulo']}</div>
                        <div class="podcast-desc">{podcast['descripcion'][:60]}{'...' if len(podcast['descripcion']) > 60 else ''}</div>
                        {video_embed if is_youtube else f'<audio controls style="width: 100%; margin: 10px 0;"><source src="{url}" type="audio/mpeg">Tu navegador no soporta el elemento de audio.</audio>'}
                        <div class="podcast-desc">Duración: {podcast['duracion'] if 'duracion' in podcast.keys() else 'N/A'} | Categoría: {podcast['categoria'] if 'categoria' in podcast.keys() else 'General'}</div>
                        <button class="like-btn" onclick="window.location.reload()">❤️ {podcast['likes'] if 'likes' in podcast.keys() else 0}</button>
                    </div>
                    ''', unsafe_allow_html=True)
            if i + 4 < len(podcasts):
                st.markdown("---")
    else:
        st.markdown('''
        <div class="podcast-item" style="text-align:center;">
            <h3>📻 Próximamente...</h3>
            <p>Estamos preparando contenido de podcast exclusivo para ti. 
            ¡Mantente atento a las actualizaciones!</p>
        </div>
        ''', unsafe_allow_html=True)
