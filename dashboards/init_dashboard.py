import sqlite3

DB_NAME = "db/beyond_platform.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def get_top_videos(limit=4):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM videos ORDER BY likes DESC LIMIT ?", (limit,))
    videos = c.fetchall()
    conn.close()
    return videos

def get_top_podcasts(limit=4):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM podcasts ORDER BY id DESC LIMIT ?", (limit,))
    podcasts = c.fetchall()
    conn.close()
    return podcasts

import streamlit as st
import os
import base64

def show():

    local_img = "assets/images/image1.jpg"
    if os.path.exists(local_img):
        with open(local_img, "rb") as img_file:
            img_base64 = base64.b64encode(img_file.read()).decode()
        img_src = f"data:image/jpeg;base64,{img_base64}"
    else:
        img_src = "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80"

    # Título dentro de la caja gris
    titulo_html = """
    <span style='font-size:25px; font-weight:bold; color:#7c82ce; text-align:center; font-family:Roboto Condensed,Arial,sans-serif; margin-bottom:18px; display:block;'>¿QUÉ ES BEYOND PLATFORM?</span>
    """
    # Obtener los 4 videos más votados
    videos = get_top_videos(4)

    # Mostrar los 4 podcasts más recientes como videos de YouTube
    podcasts = get_top_podcasts(4)

    # HERO FIJO: mostrar siempre el video solicitado
    hero_iframe = '<iframe src="https://www.youtube.com/embed/qizz5T8Zc48" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="width:100%; height:100%; border:none; background:#000;"></iframe>'

    st.markdown(f"""
    <style>
    .beyond-title-hero {{
        font-size: 40px;
        font-weight: bold;
        color: #7c82ce;
        text-align: center;
        margin-bottom: 0px;
        margin-top: 24px;
        letter-spacing: 0.01em;
        font-family: 'Roboto Condensed', Arial, sans-serif;
    }}
    .fullwidth-row {{
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
    }}
    .fullwidth-row > div {{
        flex: 1 1 0;
        min-width: 0;
        padding: 0;
        margin: 0;
    }}
    .fullwidth-row iframe, .fullwidth-row img {{
        display: block;
        width: 100%;
        height: 60vh;
        max-height: 90vh;
        border-radius: 0;
        margin: 0;
        padding: 0;
        object-fit: cover;
    }}
    @media (max-width: 900px) {{
        .fullwidth-row iframe, .fullwidth-row img {{
            height: 40vh;
        }}
    }}
    @media (max-width: 600px) {{
        .fullwidth-row {{
            flex-direction: column;
        }}
        .fullwidth-row iframe, .fullwidth-row img {{
            height: 30vh;
        }}
    }}
    .info-box-below-hero {{
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
    }}
    .info-box-below-hero > div {{
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
    }}
    .info-box-below-hero > div:first-child {{
        align-items: center;
        flex-basis: 40%;
        max-width: 40%;
    }}
    .info-box-below-hero > div:last-child {{
        align-items: center;
        justify-content: center;
        flex-basis: 60%;
        max-width: 60%;
        text-align: center;
    }}
    @media (max-width: 900px) {{
        .info-box-below-hero {{
            flex-direction: column;
        }}
        .info-box-below-hero > div {{
            padding: 18px 10px 18px 10px;
            flex-basis: 100%;
            max-width: 100%;
            align-items: center !important;
        }}
    }}
    @media (max-width: 900px) {{
        .info-box-below-hero > div {{
            padding: 18px 10px 18px 10px;
        }}
    }}
    </style>
    <div class="fullwidth-row">
        <div>
            {hero_iframe}
        </div>
        <div>
            <img src="{img_src}" alt="Imagen principal" style="width:100%; height:100%; object-fit:cover; border:none; background:#eee; display:block;" />
        </div>
    </div>
    <div class="info-box-below-hero">
        <div>{titulo_html}</div>
        <div>
            Beyond Platform está pensada para quienes<br>
            creen que la verdadera transformación de las<br>
            sociedades nace de personas apasionadas por<br>
            la educación y la innovación desde diferentes<br>
            puntos de contacto y que son capaces de<br>
            inspirar al mundo con sus acciones.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Mostrar las 4 charlas más votadas en miniatura
    videos = get_top_videos(4)
    st.markdown('<div style="font-size:2rem; color:#7c82ce; font-weight:bold; text-decoration:underline; font-family:Roboto Condensed,Arial,sans-serif; margin:32px 0 18px 0; text-align:left;">Charlas</div>', unsafe_allow_html=True)
    st.markdown("""
    <style>
    .charla-thumb {
        background: #fff;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.07);
        padding: 12px 8px 18px 8px;
        margin-bottom: 18px;
        display: flex;
        flex-direction: column;
        align-items: center;
        min-height: 260px;
    }
    .charla-thumb img {
        width: 100%;
        max-width: 180px;
        min-height: 100px;
        border-radius: 8px;
        margin-bottom: 10px;
        object-fit: cover;
        background: #eee;
    }
    .charla-title {
        font-size: 1.1rem;
        font-weight: bold;
        color: #333;
        text-align: center;
        margin-top: 6px;
    }
    </style>
    """, unsafe_allow_html=True)
    import re
    if 'selected_video' not in st.session_state:
        st.session_state['selected_video'] = None
    cols = st.columns(4)
    for idx, video in enumerate(videos):
        with cols[idx % 4]:
            import re
            yt_match = re.search(r"(?:v=|youtu.be/|embed/)([\w-]+)", video["url"])
            yt_id = yt_match.group(1) if yt_match else "ZNn2MBdliow"
            st.markdown(f"""
                <div class='charla-thumb'>
                    <iframe width="100%" height="200" src="https://www.youtube.com/embed/{yt_id}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                    <div class='charla-title'>{video['titulo']}</div>
                </div>
            """, unsafe_allow_html=True)

    # Sección de podcasts
    st.markdown('<div style="font-size:2rem; color:#7c82ce; font-weight:bold; text-decoration:underline; font-family:Roboto Condensed,Arial,sans-serif; margin:32px 0 18px 0; text-align:left;">Podcasts</div>', unsafe_allow_html=True)
    cols_pod = st.columns(4)
    for idx, podcast in enumerate(podcasts):
        with cols_pod[idx % 4]:
            import re
            yt_match = re.search(r"(?:v=|youtu.be/|embed/)([\w-]+)", podcast["url"])
            yt_id = yt_match.group(1) if yt_match else "ZNn2MBdliow"
            st.markdown(f"""
                <div class='charla-thumb'>
                    <iframe width="100%" height="200" src="https://www.youtube.com/embed/{yt_id}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                    <div class='charla-title'>{podcast['titulo']}</div>
                </div>
            """, unsafe_allow_html=True)
