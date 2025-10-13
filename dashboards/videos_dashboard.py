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

def like_video(video_id):
    """Increment the like count for a video."""
    conn = get_db()
    c = conn.cursor()
    c.execute("UPDATE videos SET likes = likes + 1 WHERE id = ?", (video_id,))
    conn.commit()
    conn.close()

def get_share_url(video_url):
    """Generate a shareable URL for the video."""
    return video_url

def show():
    # Unificar estilos visuales con la home
    st.markdown("""
    <style>
    .video-title {
        font-size: 24px;
        font-weight: bold;
        color: #7c82ce;
        text-align: left;
        margin-bottom: 20px;
    }
    .video-card {
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
        margin-bottom: 15px;
        padding: 15px;
        background-color: #f8f9fa;
    }
    .video-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    .video-thumbnail {
        border-radius: 10px;
        width: 100%;
        margin-bottom: 10px;
    }
    .video-desc {
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

    # Get all videos from database
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM videos ORDER BY likes DESC, descripcion ASC")
    videos = c.fetchall()
    conn.close()

    # Título principal
    st.markdown('<div class="video-title">CHARLAS</div>', unsafe_allow_html=True)
    st.markdown("---")
    if videos:
        # Mostrar videos en tarjetas de 4 columnas como en la home
        for i in range(0, len(videos), 4):
            group = videos[i:i+4]
            cols = st.columns(4)
            for col, video in zip(cols, group):
                with col:
                    video_url = video['url']
                    if 'youtube.com/watch?v=' in video_url:
                        video_id = video_url.split('watch?v=')[-1].split('&')[0]
                    elif 'youtu.be/' in video_url:
                        video_id = video_url.split('youtu.be/')[-1].split('?')[0]
                    else:
                        video_id = None
                    if video_id:
                        thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
                        st.markdown(f'''
                        <div class="video-card">
                            <a href="{video_url}" target="_blank">
                                <img src="{thumbnail_url}" class="video-thumbnail" alt="{video['titulo']}">
                            </a>
                            <div class="video-desc">{video['titulo']}</div>
                            <div class="video-desc">{truncate_text(video['descripcion'] or '', 60)}</div>
                            <button class="like-btn" onclick="window.location.reload()">❤️ {video['likes'] or 0}</button>
                        </div>
                        ''', unsafe_allow_html=True)
                    else:
                        st.markdown(f"**{video['titulo']}**")
                        st.markdown(f"[Ver video]({video_url})")
            if i + 4 < len(videos):
                st.markdown("---")
    else:
        st.markdown('''
        <div class="video-card" style="text-align:center;">
            <h3>🎬 Próximamente</h3>
            <p>Estamos preparando contenido increíble para ti.</p>
            <p>¡Mantente atento a nuestros próximos lanzamientos!</p>
        </div>
        ''', unsafe_allow_html=True)